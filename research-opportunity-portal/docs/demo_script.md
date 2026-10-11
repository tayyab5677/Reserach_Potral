# Demo Video Script (60 Seconds)

> **Instructions:** Follow this script while screen-recording. Keep it brisk — each step should take about 5–8 seconds.

---

## [0:00 – 0:05] Backend Running

> _Show the terminal._

"The Flask backend is running on localhost port 5000. It connects to a MySQL database called `research_portal`."

---

## [0:05 – 0:10] Frontend Running

> _Switch to the browser showing the portal._

"Here's the frontend — a dark-themed single-page application. It loads all opportunities from the API automatically."

---

## [0:10 – 0:20] Create a New Opportunity

> _Click "New Opportunity", fill in the form quickly, submit._

"Let's create a new research opportunity. I'll fill in the title, research area, faculty name, department, skills, description, positions, and deadline. Click Create — and we see a success message."

---

## [0:20 – 0:27] List View

> _Show the card grid with the new opportunity visible._

"The new opportunity appears in the list alongside the existing ones. We can filter by Open or Closed status."

---

## [0:27 – 0:35] Update an Opportunity

> _Click a card to view details → Click Edit → Change a field → Submit._

"Let me view the details of this opportunity. I'll click Edit, update the title and positions, and save. The changes reflect immediately."

---

## [0:35 – 0:42] Close an Opportunity

> _From the detail view, click the Close button._

"I can also close an opportunity by clicking the Close button. The status badge changes from Open to Closed."

---

## [0:42 – 0:48] Delete with Confirmation

> _Click Delete → Confirm in the modal._

"To delete, I click Delete. A confirmation dialog appears — I confirm, and the opportunity is removed."

---

## [0:48 – 0:55] Validation / Error Handling

> _Either: submit an empty form (client-side), or show a 404 in Postman._

"If I try to submit an empty form, client-side validation highlights the missing fields. And in Postman, requesting a deleted ID returns a 404 error with a clear JSON message."

---

## [0:55 – 1:00] Postman API Testing

> _Show Postman with a successful GET request and the JSON response._

"Finally, here's the Postman collection. Each endpoint returns proper status codes and JSON responses. That covers the full CRUD lifecycle of the Research Opportunity Portal."

---

> **Total: ~60 seconds**
