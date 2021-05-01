/* Global Variables */
const feelings = document.querySelector('#feelings');
const zipCode = document.querySelector('#zip');
const generateButton = document.querySelector('#generate');

const getDate = document.querySelector('#date');
const getTemp = document.querySelector('#temp');
const getContent = document.querySelector('#content');

const getError = document.querySelector('#error');
// Create a new date instance dynamically with JS
let d = new Date();
// let newDate = `${d.getMonth()}.${d.getDate()}.${d.getFullYear()}`;

var feelingsValue, zipCodeValue;
// component to setup the weather API
const baseUrl = 'http://api.openweathermap.org/data/2.5/weather?zip='
const apiKey = '&appid=ad87a9892b483707db89a3b1940078af';



// fetch the data from the api on -> (openweathermap.org)
const getApiData = async (url='', code='', key='') => {
		// fetch the url
		const response = await fetch(url+code+key); 
		// get the data into json format
		try {
			const dataObj = await response.json();   
			return dataObj;
		} 
		// throw an error if there are any craches
		catch (error) {
			console.log(error);    
		}
}

// post the returned data to ('/add') url
const postData = async (url = '', data = {}) => {
  	const response = await fetch(url, {
    	method: "POST",
    	credentials: "same-origin",
    	headers: {
      		"Content-Type": "application/json"
    	},
	    body: JSON.stringify(data)
  });

  try {
    const newData = await response.json();
    return newData;
  }
  catch (error) {
    console.log(error);
  }
};

// Update the UI for index page 
const UpdateUi = async(url='') => {
	const response = await fetch(url);

	try {
		// get the data
		const data = await response.json();
		// update the html page
		getDate.innerHTML = `Date & Time: ${data.date}`
		getTemp.innerHTML = `Temprature: ${data.temp}`
		getContent.innerHTML = `Feelings: ${data.content}`
		getError.innerHTML = ""

	} catch(error) {
		console.log('error' + error);
	}
}

// click eventListener
generateButton.addEventListener('click', (e)=>{
	feelingsValue = feelings.value;
	zipCodeValue = zipCode.value;


	getApiData(baseUrl, zipCodeValue, apiKey)
	// after getting the data successfully POST it  to the (/add) url
	.then((dataObj) => {
		// handle the returned data
		const newDataObj = {
			date: d,
			temp: dataObj['main']['temp'],
			content: feelingsValue
		}
		// post the new data to ('/add') url
		postData('/add', newDataObj)
		// after posting the data successfully update the UI
		.then(() => {
			UpdateUi('/all');
		})	
	}) 
	// print an error into console if there are any craches
	.catch((error) => {
		getError.innerHTML = "error 404: City for that Zip Code doesn't exist";
	  	getDate.innerHTML = ""
		getTemp.innerHTML = ""
		getContent.innerHTML = ""
		console.log('error' + error);
	});

})
