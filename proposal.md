# Project Proposal: Day-2-Day

## Project Vision Statement
Day-2-Day will empower students and workers to take control of their schedules by providing an intuitive, desktop-native task management application that seamlessly integrates with Canvas LMS, transforming scattered assignments and commitments into an organized, actionable daily plan.

## Project Overview

Day-2-Day is a comprehensive calendar and task management application designed specifically for students and working professionals who need to organize their academic assignments, work tasks, and personal commitments in one centralized location. The application will serve as a powerful organizational tool that goes beyond simple calendar functionality by integrating directly with Canvas LMS to automatically sync course assignments and due dates, while also allowing users to add custom tasks, notes, and reminders.

## Problem Statement

Students and workers often struggle to manage multiple commitments across different platforms and systems. Canvas provides assignment information, but lacks robust task management features. External calendar applications don't integrate with educational platforms. Students frequently miss deadlines or feel overwhelmed because their assignments are scattered across multiple systems with no unified view of their day-to-day responsibilities. Day-2-Day addresses this gap by creating a single source of truth for all tasks and assignments, with intelligent reminders and note-taking capabilities built directly into the workflow.

## Target Audience

Our primary users are:
- **Students** using Canvas LMS who need to track assignments, projects, and study tasks
- **Working professionals** who are also students and need to balance academic and professional responsibilities
- **Organized individuals** who prefer desktop applications over web-based tools for better performance and offline access

## Core Features

### Canvas Integration
The application will leverage the Canvas API to automatically retrieve and synchronize class assignments with their due dates. This eliminates manual data entry and ensures users always have up-to-date assignment information. The integration will pull course information, assignment titles, descriptions, and deadlines, presenting them in an organized, easily digestible format within the Day-2-Day interface.

### Task Management and Organization
Users will be able to view their commitments on a day-by-day basis, with the ability to organize tasks by priority, category, or course. The application will support both Canvas-synced assignments and custom user-created tasks, allowing for comprehensive life management beyond just academic work. Each task can be marked as complete, rescheduled, or modified as needed.

### Enhanced Note-Taking
A key differentiator of Day-2-Day is the ability to add detailed notes and clarifications to individual assignments or groups of related assignments. Users can attach additional context, break down complex assignments into subtasks, add resource links, or include instructor clarifications directly within the task view. This feature transforms assignments from simple line items into actionable work items with all necessary context in one place.

### Automated Reminders
The application will include a flexible reminder system that allows users to set automated notifications for upcoming deadlines. Users can configure reminders to trigger at various intervals (1 day before, 2 days before, 3 days before, etc.) or at specific times. This proactive notification system helps prevent last-minute scrambling and missed deadlines.

## Technical Architecture

### Application Framework
The application will be built as a web application accessible through modern web browsers. The application will be hosted on a web server and accessible via URL.

### External Integration
The Canvas API will be integrated to fetch assignment data, course information, and due dates. We will implement secure authentication to access user Canvas accounts and establish regular sync intervals to keep assignment data current. The application will cache Canvas data locally for offline access and quick loading times.

### Notification System
We will implement a notification system, this will require research into notification scheduling, permission handling, and user preference management to ensure reminders are delivered reliably and non-intrusively.

## Development Approach

The project will be developed iteratively, starting with core functionality (basic task display and manual task entry) and progressively adding features (Canvas integration, reminders, enhanced notes).

## Success Criteria

The project will be considered successful when:
1. Users can successfully authenticate with Canvas and view their assignments in the application
2. Users can create, edit, and delete custom tasks
3. Users can add notes and additional context to any task or assignment
4. Users receive timely notifications for upcoming deadlines based on their preferences
5. The application runs reliably as a web application
6. The user interface is intuitive and responsive, providing a better experience than using Canvas alone


## Conclusion

Day-2-Day represents a practical solution to a real problem faced by students and working professionals. By combining Canvas integration with task management and an accessible web application format, we will create a tool that genuinely improves how users organize and complete their daily responsibilities.
