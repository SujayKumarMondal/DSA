import * as vscode from "vscode";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import * as path from "node:path";
import { buildDashboardHtml } from "./dashboard";

const execFileAsync = promisify(execFile);
const STORAGE_KEY = "codehabit.data.v1";
const DEFAULT_GOALS: Goals = { daily: 60, weekly: 300, monthly: 1200 };
const TICK_MS = 15_000;
const GIT_POLL_MS = 60_000;
const CODE_FILE_GLOB = "**/*.{py,pyi,js,jsx,ts,tsx,mjs,cjs,java,kt,go,rs,c,cc,cpp,h,hpp,cs,php,rb,swift,scala,sql,sh,ps1,html,css,vue,svelte,ipynb}";

interface Goals {
  daily: number;
  weekly: number;
  monthly: number;
}

interface TimeEntry {
  date: string;
  project: string;
  language: string;
  seconds: number;
}

interface CommitEntry {
  date: string;
  project: string;
  hash: string;
  subject?: string;
}

interface DailyMetric {
  date: string;
  project: string;
  linesChanged: number;
  editedLineKeys: string[];
  saves: number;
  focusSessions: number;
  longestSessionSeconds: number;
}

interface TaskEntry {
  id: string;
  title: string;
  project: string;
  filePath?: string;
  completedAt?: string;
}

interface TrackerData {
  sessions: TimeEntry[];
  commits: CommitEntry[];
  gitProjects: string[];
  dailyMetrics: DailyMetric[];
  tasks: TaskEntry[];
  goals: Goals;
  enabled: boolean;
}

interface WorkspaceInfo {
  uri: vscode.Uri;
  name: string;
  path: string;
}

let extensionContext: vscode.ExtensionContext;
let tracker: TrackerData;
let lastActivity = Date.now();
let lastTick = Date.now();
let dashboard: vscode.WebviewPanel | undefined;
let statusItem: vscode.StatusBarItem;
let activeFocusSession: { startedAt: number; date: string; project: string } | undefined;
let lineEditTrackingDate: string | undefined;
const editedLineKeysByProject = new Map<string, Set<string>>();
const lastGitPoll = new Map<string, number>();
const reportedGitFailures = new Set<string>();

function todayKey(date = new Date()): string {
  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0")
  ].join("-");
}

function createDefaultData(): TrackerData {
  return {
    sessions: [],
    commits: [],
    gitProjects: [],
    dailyMetrics: [],
    tasks: [],
    goals: { ...DEFAULT_GOALS },
    enabled: true
  };
}

function currentWorkspaces(): WorkspaceInfo[] {
  return (vscode.workspace.workspaceFolders ?? []).map((folder) => ({
    uri: folder.uri,
    name: folder.name,
    path: folder.uri.fsPath
  }));
}

function workspaceForUri(uri: vscode.Uri): WorkspaceInfo | undefined {
  const folder = vscode.workspace.getWorkspaceFolder(uri);
  if (!folder) {
    return undefined;
  }
  return { uri: folder.uri, name: folder.name, path: folder.uri.fsPath };
}

function relativeFile(workspace: WorkspaceInfo, uri: vscode.Uri): string {
  return path.relative(workspace.path, uri.fsPath).replace(/\\/g, "/");
}

function taskId(projectPath: string, filePath: string): string {
  return `${projectPath}::${filePath}`.toLowerCase();
}

function recordTask(workspace: WorkspaceInfo, filePath: string, title?: string): TaskEntry {
  const id = taskId(workspace.path, filePath);
  let task = tracker.tasks.find((item) => item.id === id);
  if (!task) {
    task = {
      id,
      project: workspace.path,
      filePath,
      title: title ?? path.basename(filePath).replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ")
    };
    tracker.tasks.push(task);
  }
  return task;
}

function metricsFor(date: string, project: string): DailyMetric {
  let metric = tracker.dailyMetrics.find((item) =>
    item.date === date && item.project === project
  );
  if (!metric) {
    metric = {
      date,
      project,
      linesChanged: 0,
      editedLineKeys: [],
      saves: 0,
      focusSessions: 0,
      longestSessionSeconds: 0
    };
    tracker.dailyMetrics.push(metric);
  } else {
    metric.editedLineKeys ??= [];
  }
  return metric;
}

function finishFocusSession(endedAt: number): void {
  if (!activeFocusSession) {
    return;
  }
  const seconds = Math.floor(Math.max(0, endedAt - activeFocusSession.startedAt) / 1000);
  const metric = metricsFor(activeFocusSession.date, activeFocusSession.project);
  metric.longestSessionSeconds = Math.max(metric.longestSessionSeconds, seconds);
  activeFocusSession = undefined;
}

function getActiveCodingContext(): { workspace: WorkspaceInfo; language: string } | undefined {
  if (!tracker.enabled || vscode.window.state.focused === false) {
    return undefined;
  }
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.isUntitled || editor.document.uri.scheme !== "file") {
    return undefined;
  }
  const workspace = workspaceForUri(editor.document.uri);
  if (!workspace) {
    return undefined;
  }
  return { workspace, language: editor.document.languageId || "plaintext" };
}

async function persist(): Promise<void> {
  await extensionContext.globalState.update(STORAGE_KEY, tracker);
  refreshStatus();
}

function refreshStatus(): void {
  const context = getActiveCodingContext();
  statusItem.text = "$(pulse) CodeHabit";
  if (!tracker.enabled) {
    statusItem.tooltip = "Tracking paused. Click to open the CodeHabit dashboard";
  } else if (context) {
    const minutes = Math.floor((tracker.sessions
      .filter((entry) => entry.date === todayKey())
      .reduce((total, entry) => total + entry.seconds, 0)) / 60);
    statusItem.tooltip = `${minutes} minutes today in ${context.workspace.name} · ${context.language}. Click to open the CodeHabit dashboard`;
  } else {
    statusItem.tooltip = "Tracking pauses when no workspace editor is active. Click to open the CodeHabit dashboard";
  }
}

async function tick(): Promise<void> {
  const now = Date.now();
  const elapsedMs = Math.max(0, now - lastTick);
  lastTick = now;
  const context = getActiveCodingContext();
  const idleTimeout = Math.max(1, vscode.workspace.getConfiguration("codehabit")
    .get<number>("idleTimeoutMinutes", 5)) * 60_000;
  const countedMs = context
    ? Math.min(elapsedMs, Math.max(0, lastActivity + idleTimeout - (now - elapsedMs)))
    : 0;
  if (context && countedMs > 0) {
    const seconds = Math.floor(countedMs / 1000);
    if (seconds > 0) {
      const date = todayKey();
      const entry = tracker.sessions.find((item) =>
        item.date === date &&
        item.project === context.workspace.path &&
        item.language === context.language
      );
      if (entry) {
        entry.seconds += seconds;
      } else {
        tracker.sessions.push({
          date,
          project: context.workspace.path,
          language: context.language,
          seconds
        });
      }
      if (activeFocusSession && activeFocusSession.project !== context.workspace.path) {
        finishFocusSession(now - elapsedMs);
      }
      if (!activeFocusSession) {
        activeFocusSession = {
          startedAt: now - elapsedMs,
          date,
          project: context.workspace.path
        };
        metricsFor(date, context.workspace.path).focusSessions++;
      }
      const sessionMetric = metricsFor(activeFocusSession.date, activeFocusSession.project);
      sessionMetric.longestSessionSeconds = Math.max(
        sessionMetric.longestSessionSeconds,
        Math.floor((now - elapsedMs + countedMs - activeFocusSession.startedAt) / 1000)
      );
    }
  } else if (activeFocusSession) {
    finishFocusSession(Math.min(now, lastActivity + idleTimeout));
  }
  await persist();
  await pollGit();
  if (dashboard) {
    await updateDashboard();
  }
}

async function pollGit(): Promise<void> {
  for (const workspace of currentWorkspaces()) {
    const lastPoll = lastGitPoll.get(workspace.path) ?? 0;
    if (Date.now() - lastPoll < GIT_POLL_MS) {
      continue;
    }
    const initialScan = !lastGitPoll.has(workspace.path);
    lastGitPoll.set(workspace.path, Date.now());
    try {
      const { stdout: repositoryStatus } = await execFileAsync("git", [
        "-C", workspace.path, "rev-parse", "--is-inside-work-tree"
      ], { timeout: 5_000, windowsHide: true });
      if (repositoryStatus.trim() === "true" && !tracker.gitProjects.includes(workspace.path)) {
        tracker.gitProjects.push(workspace.path);
      }
      const { stdout } = await execFileAsync("git", [
        "-C", workspace.path,
        "log",
        "--all",
        ...(initialScan ? [] : ["-n", "20"]),
        "--format=%H%x1f%ct%x1f%s"
      ], { timeout: initialScan ? 30_000 : 5_000, maxBuffer: 25 * 1024 * 1024, windowsHide: true });
      const commits = stdout.trim().split(/\r?\n/).filter(Boolean);
      for (const line of commits) {
        const [hash, timestamp, subject] = line.split("\x1f");
        if (!hash || tracker.commits.some((commit) =>
          commit.hash === hash && commit.project === workspace.path
        )) {
          continue;
        }
        tracker.commits.push({
          hash,
          project: workspace.path,
          date: todayKey(new Date(Number(timestamp) * 1000)),
          subject
        });
      }
      reportedGitFailures.delete(workspace.path);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (message.includes("not a git repository")) {
        tracker.gitProjects = tracker.gitProjects.filter((project) => project !== workspace.path);
        reportedGitFailures.delete(workspace.path);
      } else if (!message.includes("does not have any commits yet") &&
          !reportedGitFailures.has(workspace.path)) {
        reportedGitFailures.add(workspace.path);
        console.warn(`CodeHabit could not read Git history for ${workspace.path}: ${message}`);
      }
    }
  }
  await persist();
}

function dateOffset(date: Date, days: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function startOfWeek(date: Date): Date {
  const result = new Date(date);
  result.setHours(0, 0, 0, 0);
  result.setDate(result.getDate() - ((result.getDay() + 6) % 7));
  return result;
}

function secondsForDay(date: string): number {
  return tracker.sessions.reduce((total, entry) =>
    total + (entry.date === date ? entry.seconds : 0), 0);
}

function currentStreak(): number {
  const today = new Date();
  const cursor = secondsForDay(todayKey(today)) > 0 ? today : dateOffset(today, -1);
  let streak = 0;
  for (let i = 0; i < 36_600; i++) {
    const key = todayKey(dateOffset(cursor, -i));
    if (secondsForDay(key) <= 0) {
      break;
    }
    streak++;
  }
  return streak;
}

function longestStreak(): number {
  const dates = [...new Set(tracker.sessions.map((item) => item.date))].sort();
  let longest = 0;
  let current = 0;
  let previous: Date | undefined;
  for (const date of dates) {
    const parsed = new Date(`${date}T00:00:00`);
    const isNextDay = previous !== undefined &&
      Math.round((parsed.getTime() - previous.getTime()) / 86_400_000) === 1;
    current = isNextDay ? current + 1 : 1;
    longest = Math.max(longest, current);
    previous = parsed;
  }
  return longest;
}

function metricsBetween(
  fromDate: string,
  throughDate: string
): Omit<DailyMetric, "date" | "project" | "editedLineKeys"> {
  const entries = tracker.dailyMetrics.filter((item) =>
    item.date >= fromDate && item.date <= throughDate
  );
  return {
    linesChanged: entries.reduce((total, item) => total + item.linesChanged, 0),
    saves: entries.reduce((total, item) => total + item.saves, 0),
    focusSessions: entries.reduce((total, item) => total + item.focusSessions, 0),
    longestSessionSeconds: entries.reduce(
      (longest, item) => Math.max(longest, item.longestSessionSeconds), 0
    )
  };
}

function dashboardData(): Record<string, unknown> {
  const now = new Date();
  const today = todayKey(now);
  const weekStart = startOfWeek(now);
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
  const yearStart = new Date(now.getFullYear(), 0, 1);
  const todayMetrics = metricsBetween(today, today);
  const weekMetrics = metricsBetween(todayKey(weekStart), today);
  if (activeFocusSession && activeFocusSession.date === today) {
    todayMetrics.longestSessionSeconds = Math.max(
      todayMetrics.longestSessionSeconds,
      Math.floor((Date.now() - activeFocusSession.startedAt) / 1000)
    );
    weekMetrics.longestSessionSeconds = Math.max(
      weekMetrics.longestSessionSeconds,
      todayMetrics.longestSessionSeconds
    );
  }
  const monthMetrics = metricsBetween(todayKey(monthStart), today);
  const yearMetrics = metricsBetween(todayKey(yearStart), today);
  const allMetrics = metricsBetween("0000-01-01", today);
  const allTimeSeconds = tracker.sessions.reduce((total, item) => total + item.seconds, 0);
  const weekSeconds = tracker.sessions
    .filter((item) => item.date >= todayKey(weekStart) && item.date <= today)
    .reduce((total, item) => total + item.seconds, 0);
  const monthSeconds = tracker.sessions
    .filter((item) => item.date >= todayKey(monthStart) && item.date <= today)
    .reduce((total, item) => total + item.seconds, 0);
  const yearSeconds = tracker.sessions
    .filter((item) => item.date >= todayKey(yearStart) && item.date <= today)
    .reduce((total, item) => total + item.seconds, 0);
  const aggregateLanguages = (fromDate: string, throughDate: string) => {
    const totals = new Map<string, number>();
    for (const entry of tracker.sessions) {
      if (entry.date >= fromDate && entry.date <= throughDate) {
        totals.set(entry.language, (totals.get(entry.language) ?? 0) + entry.seconds);
      }
    }
    return [...totals.entries()]
      .map(([name, seconds]) => ({ name, seconds }))
      .sort((a, b) => b.seconds - a.seconds);
  };
  const heatmap = Array.from({ length: 182 }, (_, index) => {
    const date = dateOffset(now, index - 181);
    const key = todayKey(date);
    const metrics = metricsBetween(key, key);
    return { date: key, seconds: secondsForDay(key), linesChanged: metrics.linesChanged };
  });
  const tasks = [...tracker.tasks];
  const weeklyActivity = Array.from({ length: 7 }, (_, index) => {
    const date = todayKey(dateOffset(weekStart, index));
    const metrics = metricsBetween(date, date);
    return {
      date,
      seconds: secondsForDay(date),
      linesChanged: metrics.linesChanged,
      focusSessions: metrics.focusSessions
    };
  });
  const projectMap = new Map<string, {
    name: string;
    seconds: number;
    latestDate: string;
    activeDays: Set<string>;
  }>();
  for (const entry of tracker.sessions) {
    const project = projectMap.get(entry.project) ?? {
      name: path.basename(entry.project) || entry.project,
      seconds: 0,
      latestDate: entry.date,
      activeDays: new Set<string>()
    };
    project.seconds += entry.seconds;
    project.latestDate = project.latestDate > entry.date ? project.latestDate : entry.date;
    project.activeDays.add(entry.date);
    projectMap.set(entry.project, project);
  }
  const projects = [...projectMap.entries()].map(([project, entry]) => ({
    project,
    name: entry.name,
    seconds: entry.seconds,
    latestDate: entry.latestDate,
    activeDays: entry.activeDays.size
  }));
  const recentCommits = [...tracker.commits]
    .sort((a, b) => b.date.localeCompare(a.date))
    .slice(0, 8)
    .map((commit) => ({
      date: commit.date,
      project: path.basename(commit.project) || commit.project,
      subject: commit.subject ?? commit.hash.slice(0, 8)
    }));
  return {
    generatedAt: new Date().toISOString(),
    enabled: tracker.enabled,
    dailySeconds: secondsForDay(today),
    todaySeconds: secondsForDay(today),
    weekSeconds,
    monthSeconds,
    yearSeconds,
    allTimeSeconds,
    linesToday: todayMetrics.linesChanged,
    linesWeek: weekMetrics.linesChanged,
    linesMonth: monthMetrics.linesChanged,
    linesYear: yearMetrics.linesChanged,
    linesAllTime: allMetrics.linesChanged,
    savesToday: todayMetrics.saves,
    savesWeek: weekMetrics.saves,
    sessionsToday: todayMetrics.focusSessions,
    sessionsWeek: weekMetrics.focusSessions,
    longestSessionSeconds: weekMetrics.longestSessionSeconds,
    streak: currentStreak(),
    bestStreak: longestStreak(),
    goals: tracker.goals,
    commitsToday: tracker.commits.filter((item) => item.date === today).length,
    commitsWeek: tracker.commits.filter((item) =>
      item.date >= todayKey(weekStart) && item.date <= today
    ).length,
    commitsMonth: tracker.commits.filter((item) =>
      item.date >= todayKey(monthStart) && item.date <= today
    ).length,
    gitAvailable: tracker.gitProjects.length > 0,
    recentCommits,
    languages: aggregateLanguages("0000-01-01", today),
    languagesToday: aggregateLanguages(today, today),
    projects,
    weeklyActivity,
    daily: { ...todayMetrics },
    weekly: { ...weekMetrics },
    monthly: { ...monthMetrics },
    weekDays: new Set(tracker.sessions
      .filter((item) => item.date >= todayKey(weekStart) && item.date <= today)
      .map((item) => item.date)).size,
    yesterdaySeconds: secondsForDay(todayKey(dateOffset(now, -1))),
    todayDeepWorkSeconds: secondsForDay(today),
    todayProject: getActiveCodingContext()?.workspace.name,
    bestDay: weeklyActivity.reduce<{ date: string; seconds: number } | undefined>(
      (best, item) => item.seconds > (best?.seconds ?? 0) ? item : best,
      undefined
    ),
    heatmap,
    tasks: tasks.sort((a, b) =>
      Number(Boolean(a.completedAt)) - Number(Boolean(b.completedAt)) ||
      a.title.localeCompare(b.title)
    ).map((task) => ({
      ...task,
      projectName: currentWorkspaces().find((workspace) => workspace.path === task.project)?.name ??
        (path.basename(task.project) || task.project)
    })),
    taskCount: tasks.length,
    completedCount: tasks.filter((task) => task.completedAt).length,
    workspaces: [...new Set(tasks.map((task) => task.project))].map((project) => ({
      path: project,
      name: path.basename(project) || project
    }))
  };
}

async function discoverWorkspaceTasks(workspace: WorkspaceInfo): Promise<void> {
  const uris = await vscode.workspace.findFiles(
    new vscode.RelativePattern(workspace.uri, CODE_FILE_GLOB),
    "**/{node_modules,.git,.venv,venv,__pycache__,out,dist,build}/**"
  );
  for (const uri of uris) {
    const relative = relativeFile(workspace, uri);
    recordTask(workspace, relative);
  }
}

async function updateDashboard(): Promise<void> {
  if (dashboard) {
    dashboard.webview.postMessage({ type: "data", data: dashboardData() });
  }
}

async function showDashboard(): Promise<void> {
  for (const workspace of currentWorkspaces()) {
    await discoverWorkspaceTasks(workspace);
  }
  await persist();
  if (dashboard) {
    dashboard.reveal(vscode.ViewColumn.One);
    await updateDashboard();
    return;
  }
  dashboard = vscode.window.createWebviewPanel(
    "codehabit.dashboard",
    "CodeHabit Dashboard",
    vscode.ViewColumn.One,
    { enableScripts: true, retainContextWhenHidden: true }
  );
  dashboard.webview.html = buildDashboardHtml();
  dashboard.onDidDispose(() => { dashboard = undefined; });
  dashboard.webview.onDidReceiveMessage(async (message: { type: string; id?: string; completed?: boolean; text?: string }) => {
    if (message.type === "ready") {
      await updateDashboard();
    } else if (message.type === "toggleTracking") {
      if (tracker.enabled) {
        finishFocusSession(Date.now());
      }
      tracker.enabled = !tracker.enabled;
      lastTick = Date.now();
      lastActivity = lastTick;
      await persist();
      await updateDashboard();
    } else if (message.type === "setGoals") {
      await setGoals();
    } else if (message.type === "export") {
      await exportData();
    } else if (message.type === "refreshTasks") {
      try {
        for (const workspace of currentWorkspaces()) {
          await discoverWorkspaceTasks(workspace);
        }
        await persist();
        await updateDashboard();
      } catch (error) {
        const detail = error instanceof Error ? error.message : String(error);
        void vscode.window.showErrorMessage(`CodeHabit could not refresh the code checklist: ${detail}`);
      }
    } else if (message.type === "copy" && message.text) {
      await vscode.env.clipboard.writeText(message.text);
      void vscode.window.showInformationMessage("CodeHabit summary copied to clipboard.");
    } else if (message.type === "openTask" && message.id) {
      await openTask(message.id);
    } else if (message.type === "toggleTask" && message.id) {
      const task = tracker.tasks.find((item) => item.id === message.id);
      if (task) {
        task.completedAt = message.completed ? new Date().toISOString() : undefined;
        await persist();
        await updateDashboard();
      }
    }
  });
}

async function openTask(id: string): Promise<void> {
  const task = tracker.tasks.find((item) => item.id === id);
  if (!task?.filePath) {
    void vscode.window.showWarningMessage("This checklist item does not have a file path.");
    return;
  }
  const filePath = path.resolve(task.project, task.filePath);
  const relativePath = path.relative(task.project, filePath);
  if (relativePath === ".." || relativePath.startsWith(`..${path.sep}`) || path.isAbsolute(relativePath)) {
    void vscode.window.showWarningMessage("The checklist file path is outside its workspace.");
    return;
  }
  try {
    const document = await vscode.workspace.openTextDocument(vscode.Uri.file(filePath));
    await vscode.window.showTextDocument(document);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    void vscode.window.showErrorMessage(`CodeHabit could not open ${task.filePath}: ${detail}`);
  }
}

async function setGoals(): Promise<void> {
  const choice = await vscode.window.showQuickPick(
    ["Daily target", "Weekly target", "Monthly target"],
    { placeHolder: "Choose a coding-time goal to update" }
  );
  if (!choice) {
    return;
  }
  const key = choice.startsWith("Daily") ? "daily" : choice.startsWith("Weekly") ? "weekly" : "monthly";
  const value = await vscode.window.showInputBox({
    prompt: `Set your ${key} coding goal in minutes`,
    value: String(tracker.goals[key]),
    validateInput: (input) => {
      const parsed = Number(input);
      return Number.isInteger(parsed) && parsed > 0 && parsed <= 100_000
        ? undefined
        : "Enter a whole number of minutes between 1 and 100,000.";
    }
  });
  if (value !== undefined) {
    tracker.goals[key] = Number(value);
    await persist();
    await updateDashboard();
  }
}

async function exportData(): Promise<void> {
  const target = await vscode.window.showSaveDialog({
    defaultUri: vscode.Uri.file(path.join(
      vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? extensionContext.globalStorageUri.fsPath,
      "codehabit-export.json"
    )),
    filters: { "JSON files": ["json"] }
  });
  if (!target) {
    return;
  }
  await vscode.workspace.fs.writeFile(
    target,
    Buffer.from(JSON.stringify({ exportedAt: new Date().toISOString(), ...tracker }, null, 2), "utf8")
  );
  void vscode.window.showInformationMessage("CodeHabit data exported as JSON.");
}

async function markCurrentFileComplete(): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.isUntitled) {
    void vscode.window.showWarningMessage("Open a saved code file before marking it complete.");
    return;
  }
  const workspace = workspaceForUri(editor.document.uri);
  if (!workspace) {
    void vscode.window.showWarningMessage("The current file is not inside a workspace.");
    return;
  }
  const task = recordTask(workspace, relativeFile(workspace, editor.document.uri));
  task.completedAt = new Date().toISOString();
  await persist();
  await updateDashboard();
  void vscode.window.showInformationMessage(`Completed: ${task.title}`);
}

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  extensionContext = context;
  tracker = context.globalState.get<TrackerData>(STORAGE_KEY) ?? createDefaultData();
  tracker.sessions ??= [];
  tracker.commits ??= [];
  tracker.gitProjects ??= [];
  tracker.dailyMetrics ??= [];
  tracker.tasks ??= [];
  tracker.goals ??= { ...DEFAULT_GOALS };
  tracker.enabled ??= true;
  statusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 50);
  statusItem.command = "codehabit.openDashboard";
  context.subscriptions.push(statusItem);
  statusItem.show();
  const timer = setInterval(() => { void tick(); }, TICK_MS);

  context.subscriptions.push(
    vscode.commands.registerCommand("codehabit.openDashboard", showDashboard),
    vscode.commands.registerCommand("codehabit.markCurrentFileComplete", markCurrentFileComplete),
    vscode.commands.registerCommand("codehabit.setGoals", setGoals),
    vscode.commands.registerCommand("codehabit.exportData", exportData),
    vscode.commands.registerCommand("codehabit.toggleTracking", async () => {
      if (tracker.enabled) {
        finishFocusSession(Date.now());
      }
      tracker.enabled = !tracker.enabled;
      lastTick = Date.now();
      lastActivity = lastTick;
      await persist();
      await updateDashboard();
    }),
    vscode.window.onDidChangeActiveTextEditor(() => {
      lastActivity = Date.now();
      lastTick = lastActivity;
      refreshStatus();
    }),
    vscode.window.onDidChangeWindowState((state) => {
      lastTick = Date.now();
      if (state.focused) {
        lastActivity = lastTick;
      }
      refreshStatus();
    }),
    vscode.workspace.onDidChangeTextDocument((event) => {
      lastActivity = Date.now();
      const workspace = workspaceForUri(event.document.uri);
      if (!tracker.enabled || vscode.window.state.focused === false || !workspace ||
          event.document.isUntitled || event.document.languageId === "plaintext") {
        return;
      }
      const date = todayKey();
      if (lineEditTrackingDate !== date) {
        lineEditTrackingDate = date;
        editedLineKeysByProject.clear();
      }
      const metric = metricsFor(date, workspace.path);
      const editedLines = editedLineKeysByProject.get(workspace.path) ??
        new Set(metric.editedLineKeys);
      editedLineKeysByProject.set(workspace.path, editedLines);
      const filePath = relativeFile(workspace, event.document.uri);
      for (const change of event.contentChanges) {
        const lines = Math.max(
          change.range.end.line - change.range.start.line + 1,
          change.text.split(/\r\n|\r|\n/).length
        );
        for (let line = 0; line < lines; line++) {
          const key = `${filePath}:${change.range.start.line + line}`;
          if (!editedLines.has(key)) {
            editedLines.add(key);
            metric.editedLineKeys.push(key);
            metric.linesChanged++;
          }
        }
      }
    }),
    vscode.workspace.onDidSaveTextDocument((document) => {
      const workspace = workspaceForUri(document.uri);
      if (!tracker.enabled || vscode.window.state.focused === false || !workspace ||
          document.isUntitled || document.languageId === "plaintext") {
        return;
      }
      metricsFor(todayKey(), workspace.path).saves++;
      void persist();
      void updateDashboard();
    }),
    vscode.window.onDidChangeTextEditorSelection(() => { lastActivity = Date.now(); }),
    vscode.workspace.onDidChangeWorkspaceFolders(async () => {
      await pollGit();
      for (const workspace of currentWorkspaces()) {
        await discoverWorkspaceTasks(workspace);
      }
      await persist();
      await updateDashboard();
    }),
    new vscode.Disposable(() => clearInterval(timer))
  );

  lastActivity = Date.now();
  lastTick = lastActivity;
  refreshStatus();
  await pollGit();
}

export function deactivate(): void {
  if (tracker && extensionContext) {
    void extensionContext.globalState.update(STORAGE_KEY, tracker);
  }
}
