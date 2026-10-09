# CodeHabit

CodeHabit is a local-first VS Code coding tracker. It records time spent in the
focused editor, Git commits, completed code-file tasks, streaks, goals, and
language/project breakdowns in the VS Code profile on this machine.

## Dashboard

The dashboard includes:

- Daily, weekly, monthly, yearly, and all-time coding time
- Activity heatmap, daily and best streaks, focus sessions, distinct edited-line
  and save counts
- Git commit history, language and project breakdowns, and a shareable annual summary
- A searchable checklist of every matching code file discovered in open workspaces,
  with completion, workspace, folder, and sort filters
- JSON export of all locally stored tracker data

Time is counted only while VS Code is focused with a saved workspace file open.
Editing, moving the cursor, and scrolling in the editor reset the idle timer;
tracking pauses after the configured idle timeout. Switching between saved
workspace files does not discard the current tracking interval. Data stays in
the local VS Code extension profile. CodeHabit does not
create an account, send telemetry, or require an internet connection.
Distinct edited-line, save, and focus-session metrics begin accumulating after
the updated extension is installed; earlier coding-time, commit, and checklist
data is retained.

## Development

Open this folder in VS Code and run the **Run CodeHabit Extension** launch
configuration (F5). The extension entry point is `src/extension.ts`; the dashboard
view is in `src/dashboard.ts`. `npm run check` type-checks the project, and
`npm run compile` builds it into `out/`.

## Install CodeHabit in VS Code

From this folder, run:

```sh
npm install
npm run package
```

This creates `codehabit-0.1.1.vsix`. In VS Code, open the Extensions view,
select the **...** menu, choose **Install from VSIX...**, and select that file.
Reload VS Code if prompted. Click the **CodeHabit** status-bar item or run
**CodeHabit: Open Dashboard** from the Command Palette (`Ctrl+Shift+P`) to open
the dashboard. The dashboard's checklist **Refresh files** button rescans every
currently open workspace.

To publish CodeHabit on the VS Code Marketplace instead, it needs to be
published under a Marketplace publisher account; the generated VSIX is for
local installation and sharing.

## View or export your data

Open the dashboard to view your coding time, activity, commits, languages,
projects, and task progress. To save all locally stored tracker records, select
**Export JSON** in the dashboard or run **CodeHabit: Export Data as JSON** from
the Command Palette. Choose where to save `codehabit-export.json`; open that
file in VS Code or another JSON viewer to inspect it.

Tracker data stays in the VS Code profile on this machine. Installing the VSIX
does not transfer data from another machine or VS Code profile.
