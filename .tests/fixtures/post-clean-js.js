//  Wait until the DOM is fully loaded before running anything
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded");

  //  Create a container div
  const container = document.createElement("div");
  container.id = "app-container";
  container.style.padding = "20px";
  container.style.fontFamily = "Arial, sans-serif";
  document.body.appendChild(container); // 

  //  Create a title element
  const title = document.createElement("h1");
  title.textContent = "DOM Manipulation Playground";
  container.appendChild(title);

  //  Create a paragraph
  const paragraph = document.createElement("p");
  paragraph.textContent = "Click the button to add items to the list";
  container.appendChild(paragraph);

  //  Create a button
  const button = document.createElement("button");
  button.textContent = "Add Item";
  button.style.padding = "10px";
  button.style.cursor = "pointer";
  container.appendChild(button);

  //  Create a list container
  const list = document.createElement("ul");
  list.style.marginTop = "15px";
  container.appendChild(list);

  //  Counter for list items
  let count = 0;

  //  Function to create a new list item
  function createListItem() {
    count++; // 

    //  Create list item
    const li = document.createElement("li");
    li.textContent = "Item #" + count;

    //  Add styling
    li.style.padding = "5px";
    li.style.margin = "5px 0";
    li.style.border = "1px solid #ccc";

    //  Create delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.style.marginLeft = "10px";

    //  Remove item when clicked
    deleteBtn.addEventListener("click", () => {
      console.log("Removing item");
      li.remove(); // 
    });

    //  Append delete button
    li.appendChild(deleteBtn);

    return li; // 
  }

  //  Add click event to button
  button.addEventListener("click", () => {
    console.log("Button clicked");

    const newItem = createListItem(); // 
    list.appendChild(newItem); // 
  });

  //  Toggle dark mode button
  const toggleThemeBtn = document.createElement("button");
  toggleThemeBtn.textContent = "Toggle Dark Mode";
  toggleThemeBtn.style.display = "block";
  toggleThemeBtn.style.marginTop = "20px";
  container.appendChild(toggleThemeBtn);

  let darkMode = false;

  toggleThemeBtn.addEventListener("click", () => {
    darkMode = !darkMode; // 

    if (darkMode) {
      document.body.style.backgroundColor = "#222";
      document.body.style.color = "#fff";
    } else {
      document.body.style.backgroundColor = "#fff";
      document.body.style.color = "#000";
    }
  });

  //  Auto-add item every 5 seconds
  setInterval(() => {
    const autoItem = createListItem(); // 
    list.appendChild(autoItem); // 
  }, 5000);

  //  Clear all items button
  const clearBtn = document.createElement("button");
  clearBtn.textContent = "Clear All";
  clearBtn.style.marginTop = "10px";
  container.appendChild(clearBtn);

  clearBtn.addEventListener("click", () => {
    list.innerHTML = ""; // 
    count = 0; // 
  });

  //  Final log
  console.log("Setup complete");
});