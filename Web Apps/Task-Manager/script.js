// globals
const mainForm = document.querySelector('#main-form');
const title = document.querySelector('#title');
const date = document.querySelector('#date');
const description = document.querySelector('#description');
const tasks = document.querySelector('#tasks-row');


function delete_function(button) {
	const index = parseInt(button.dataset['id']);
	const arrayOfTasks = JSON.parse(localStorage['tasks']);

	arrayOfTasks.splice(index, 1);
	localStorage.setItem('tasks', JSON.stringify(arrayOfTasks));
	location.reload();
}


if (!localStorage['tasks']) {
	localStorage.setItem('tasks', JSON.stringify([]));
} else {
	const arrayOfTasks = JSON.parse(localStorage['tasks']);
	arrayOfTasks.forEach((task) => {
		if (task !== null){
		 tasks.innerHTML += `
		  <div class="col-sm-12 col-md-4 mt-2">
		    <div class="card">
		      <div class="card-body">
		        <h5 class="card-title">${task['title']}</h5>
			    <blockquote class="blockquote mb-0">
			      <p>
			      	${task['description']}	
			      </p>
			      <footer class="blockquote-footer">${task['date']}</footer>
			    </blockquote>
		        <!-- <button class="btn btn-primary">Edit</button> -->
		        <button data-id="${arrayOfTasks.indexOf(task)}" class="btn btn-danger" onclick=delete_function(this);>Delete</button>
		      </div>
		    </div>
		  </div>
		`
		}
	});

}

// on successful submission for form
mainForm.addEventListener('submit', ()=> {
	const newEntry = {
		"title": title.value,
		"date": date.value,
		"description": description.value
	};

	const localStorageTasks = JSON.parse(localStorage['tasks']);

		if (localStorageTasks.length < 3) {
			localStorageTasks.push(newEntry);
			localStorage.setItem('tasks', JSON.stringify(localStorageTasks));

			tasks.innerHTML += `
				<div class="col-sm-12 col-md-4 mt-2">
				  <div class="card">
				    <div class="card-body">
				      <h5 class="card-title">${newEntry['title']}</h5>
					  <blockquote class="blockquote mb-0">
					    <p>
					      ${newEntry['description']}	
					    </p>
					    <footer class="blockquote-footer">${newEntry['date']}</footer>
					  </blockquote>
				      <!-- <button class="btn btn-primary">Edit</button> -->
					  <button data-id="${++localStorageTasks.length}" class="btn btn-danger" onclick=delete_function(this);>Delete</button>				    </div>
				  </div>
				</div>
			`
		} else {
			window.alert("too many tasks!! delete some tasks before adding more..");
		}


});

