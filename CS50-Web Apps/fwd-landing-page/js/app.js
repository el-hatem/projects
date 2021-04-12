/**
 * 
 * Manipulating the DOM exercise.
 * Exercise programmatically builds navigation,
 * scrolls to anchors from navigation,
 * and highlights section in viewport upon scrolling.
 * 
 * Dependencies: None
 * 
 * JS Version: ES2015/ES6
 * 
 * JS Standard: ESlint
 * 
*/

/**
 * Define Global Variables
 * 
*/
const sectionList = document.querySelectorAll('.section');
const nav = document.querySelector('#navbar__list');
/**
 * End Global Variables
 * Start Helper Functions
 * 
*/

/*Creates links depend on number of sections*/
function createHyperLink(content, attributes){
	const a = document.createElement('a');

	for( attr of attributes){  
		a.setAttribute(attr["name"], attr["value"]);   // set attributes for that link;
	}
	a.innerHTML = content;    // name of the section 

	return a;
}

function activateAnimation(section) {
	if (!section.classList.contains("your-active-class")) {
		section.classList.toggle("your-active-class");
	}
}

function disableAnimation(section) {
	if (section.classList.contains("your-active-class")) {
		section.classList.toggle("your-active-class");
	}
}
/**
 * End Helper Functions
 * Begin Main Functions
 * 
*/

// build the nav
function buildNav(sections) {
	sections.forEach(section => {
		// for eavery section retrieve its => (name, id)
		const sectionName = section.getAttribute('data-nav');
		const sectionId = section.id;
		// create list of linkes
		const li = document.createElement('li');
		const attributes = [
					{"name": "name", "value": `${sectionId}`},
					{"name": "class", "value": `menu__link`}
				]
		// append all links to navBar 
		li.append(createHyperLink(sectionName, attributes));
		nav.append(li);  
		
	})
}

// Add class 'active' to section when near top of viewport
var scrollListener = function() {
  sectionList.forEach(function(section) {
    var bounds = section.getBoundingClientRect();
    if (bounds.top > 0 && bounds.top < window.innerHeight) {
    	activateAnimation(section);
    } else {
    	disableAnimation(section);
    }
  });
};
// Scroll to anchor ID using scrollTO event
function scroll(event) {
	// define the actual element we have to scroll
   	const clicked = document.querySelector(`#${event.target.getAttribute('name')}`);
	var bodyRect = document.body.getBoundingClientRect(),
	    elemRect = clicked.getBoundingClientRect(),
	    offset   = [(elemRect.top - bodyRect.top), (elemRect.left - bodyRect.left)];
	//Scroll to anchor ID using scrollTO event
   	window.scrollTo({
   		"top": offset[0],
   		"left": offset[1],
   		"behavior": "smooth"
   	})
}
/**
 * End Main Functions
 * Begin Events
 * 
*/

// Build menu 
window.addEventListener('load', (e) => {buildNav(sectionList);});
// Scroll to section on link click
nav.addEventListener('click', (e) => {scroll(e);});
// Set sections as active
window.addEventListener("scroll", scrollListener);
