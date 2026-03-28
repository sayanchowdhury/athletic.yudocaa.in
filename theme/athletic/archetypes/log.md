---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
type: "strength"       # strength | cardio | rest | mobility
duration: 50           # minutes
weight:                # kg — morning fasted weight
waist:                 # cm — measure Sunday only
hevy_url: ""           # paste Hevy share URL here

workout:
  - exercise: "Exercise Name"
    sets:
      - { set: 1, weight: 0, reps: 10, warmup: true }
      - { set: 2, weight: 0, reps: 8 }
      - { set: 3, weight: 0, reps: 8, note: "" }

nutrition:
  calories: 0
  protein: 0
  carbs: 0
  fat: 0

body:
  weight:        # kg
  waist:         # cm — optional, Sunday only
  sleep:         # hours
  energy:        # /10

meals:
  - { name: "Oats + whey + banana", protein: "32g" }
  - { name: "Brown chana sprouts", protein: "10g" }
  - { name: "Lunch", protein: "" }
  - { name: "Green moong sprouts", protein: "8g" }
  - { name: "Pre-workout shake", protein: "24g" }
  - { name: "Dinner", protein: "" }
---

Notes from today's session.
