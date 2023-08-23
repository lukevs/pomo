# pomo 🍅

> A small pomodoro + vim tool

```
2021-08-18

Goals:
- ✅ Finish database
- Call back Steve
- Create new blog site
  - ✅ Update SSR
  - Find a template
  - Create the site
  - Deploy
  - Write first post


9:00 - 5:00

Planning
-

✅ Work on database
-

✅ Update SSR
-

📌 Call back Steve
-

🥪 Lunch
-

Find a template
-
-

Create the site
-
-

Deploy
-

Write first post
-
-

Free time
-
-
-
-
```

## Usage

Create a new day doc from 8:30 AM to 5 PM:
```
pomo 8.5 5
```

which opens a file in vim with a dash for each pomodoro:
```
2021-08-18

Goals:


8:30 - 5:00

Planning
-

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
```

Open your existing day's doc
```
pomo
```

View your pomo from 3 days ago
```
pomo -m 3
```

View your week goals, or create a new one for this week
```
pomo -w
```

View your global list of tasks
```
pomo -l
```

## Install

Clone this repo
```
git clone github.com/lukevs/pomo
```

Install with [pipx](https://github.com/pypa/pipx)
```
pipx install .
```
