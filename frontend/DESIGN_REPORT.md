# Frontend Design Report

## Overview
The frontend for InitGuard is designed with a focus on **minimalism, clarity, and elegance**. It provides a distraction-free interface for managing database backup tasks. The application supports both Light and Dark modes to accommodate user preferences and working environments.

## Color Scheme

The color palette is derived from Tailwind CSS's default palette, chosen for its professional and clean aesthetic.

### Light Mode (Day)
*   **Background**: `gray-50` (#f9fafb) - A soft, off-white background to reduce glare.
*   **Surface (Cards/Modals)**: `white` (#ffffff) - Clean white for content containers.
*   **Text (Primary)**: `gray-900` (#111827) - Almost black for high readability.
*   **Text (Secondary)**: `gray-500` (#6b7280) - Muted gray for labels and secondary information.
*   **Accent/Primary Action**: `blue-600` (#2563eb) - A strong, trustworthy blue for primary buttons and active links.
*   **Borders**: `gray-200` (#e5e7eb) - Subtle borders for separation.

### Dark Mode (Night)
*   **Background**: `gray-900` (#111827) - Deep dark blue-gray to minimize eye strain.
*   **Surface (Cards/Modals)**: `gray-800` (#1f2937) - Slightly lighter dark gray for content containers to provide depth.
*   **Text (Primary)**: `white` (#ffffff) - Pure white for maximum contrast against dark backgrounds.
*   **Text (Secondary)**: `gray-400` (#9ca3af) - Light gray for secondary text.
*   **Accent/Primary Action**: `blue-500` (#3b82f6) - A slightly lighter blue to stand out against the dark background.
*   **Borders**: `gray-700` (#374151) - Dark borders to define structure without being intrusive.

## Design Principles

1.  **Minimalism**:
    *   **Whitespace**: Generous use of padding and margins (`p-8`, `space-y-6`) creates a breathable layout.
    *   **Typography**: Clean sans-serif font (system default via Tailwind) ensures readability. Headers use bold weights (`font-bold`, `font-extrabold`) to establish hierarchy.
    *   **Visual Noise Reduction**: Avoided unnecessary shadows, gradients, or complex graphics. Shadows are used sparingly (`shadow-md`) only to lift cards off the background.

2.  **Responsiveness**:
    *   The layout is fully responsive, using a max-width container (`max-w-7xl`, `max-w-md`) that centers content on larger screens and adapts to mobile devices via `sm:` breakpoints.

3.  **Usability**:
    *   **Feedback**: Form errors are displayed clearly in red alert boxes.
    *   **Navigation**: A simple top navigation bar provides access to key features (Dashboard, Create Resource, Create Task).
    *   **Consistency**: Reusable components (`Button`, `Input`) ensure consistent styling across the application.

## Component Structure

*   **Layout**: Wraps all authenticated pages, providing the Navbar and consistent page padding.
*   **Navbar**: Contains the logo, navigation links, theme toggle, and logout button. It adapts its content based on authentication state.
*   **AuthContext**: Manages user session and JWT token storage in `localStorage`.
*   **ThemeContext**: Manages the `dark` class on the `<html>` element and persists preference in `localStorage`.
*   **Pages**:
    *   `Dashboard`: A clean table view of tasks with status indicators (colored badges).
    *   `CreateResource`: A dynamic form that adapts based on the selected resource type (Database vs. OSS).
    *   `CreateTask`: A form that fetches available resources to populate dropdowns, simplifying task creation.
