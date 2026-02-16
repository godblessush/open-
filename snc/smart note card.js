let input = document.getElementById("input");
let button = document.getElementById("btn");
let list = document.getElementById("noteList");
let uls = document.getElementById("uls");


button.addEventListener("click", addNote);

function addNote() {
    let userText = input.value;

    if (userText === "") {
        alert("Please enter something");
        return;
    }

 let li = document.createElement("li");
li.className = "card";

let textSpan = document.createElement("span");
textSpan.textContent = userText;

let delBtn = document.createElement("button");
delBtn.textContent = "Delete";
delBtn.className = "deleteBtn";

delBtn.onclick = function() {
    li.remove();
};

li.appendChild(textSpan);
li.appendChild(delBtn);
list.appendChild(li);


    input.value = ""; // clear input after adding
}

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        addNote();
    }
});
