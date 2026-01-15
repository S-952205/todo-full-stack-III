---
name: nextjs-ui-api-skill
description: Use when building React components or fetching data to ensure responsive design and JWT-secured communication.
---

# NextJS UI & API Skill

## Instructions
1. **Responsive UI**: Use Tailwind CSS (flex/grid) to ensure layouts work on all screen sizes.
2. **Secure Fetch**: Wrap all API calls in a function that automatically injects `Authorization: Bearer <token>` from Better Auth.
3. **UX Feedback**: Implement loading skeletons and toast notifications for API success/error states.
4. **Type Safety**: Define TypeScript interfaces for Task and User objects to prevent runtime errors.

## Examples
- **Tailwind**: `<div class="grid grid-cols-1 md:grid-cols-2 gap-4">`
- **Auth Header**: `headers: { 'Authorization': `Bearer ${token}` }`