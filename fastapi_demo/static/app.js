
var BACKEND = "";
import('./env.js')
  .then((module) => {
    // Do something with the module.
      BACKEND = module.API_URL
  });

var doPost = (payload, path) => {
    const request = new Request(BACKEND + path, {method: 'POST', body: JSON.stringify(payload)});
        fetch(request).then(response => {
    if (response.status === 200) {
        console.log(response)
    } else {
      throw new Error('Something went wrong on api server!');
    }
  })
  .then(response => {
    console.debug(response);
    // ...
  }).catch(error => {
    console.error(error);
  });
};

var doGet = (path, callback) => {
    const request = new Request(BACKEND + path, {method: 'GET'});
    return fetch(request).then(response => {
    if (response.status === 200) {
        console.log(response);
        callback(response)
    } else {
      throw new Error('Something went wrong on api server!');
    }
  })
  .then(response => {
    console.debug(response);
    // ...
  }).catch(error => {
    console.error(error);
  });
};

var setVal = async (response, id)  => {
        console.log(response)
         document.getElementById(id).innerHTML = await response.text();
};

var onSubmit = ( form ) => {
    var formData = new FormData(form);

    var payload = {
        name: formData.get("name").toString(),
        team_description: formData.get("team_description").toString(),
        open_port: formData.get("open_port"),
        ip_addr: formData.get("ip_addr")
    };

    console.log( payload );
    doPost(payload, "/competitors/");
    updateUsersTable();
    return false; //don't submit
};

function addRow(tableID, userObj) {
  // Get a reference to the table
  let tableRef = document.getElementById(tableID);
    console.log(tableRef.rows );

  // Insert a row at the end of the table
  let newRow = tableRef.insertRow(-1);

  newRow.insertCell(0).appendChild(document.createTextNode(userObj.id.toString()));
  newRow.insertCell(1).appendChild(document.createTextNode(userObj.name.toString()));
  newRow.insertCell(2).appendChild(document.createTextNode(userObj.team_description.toString()));
  newRow.insertCell(3).appendChild(document.createTextNode(userObj.open_port.toString()));
  newRow.insertCell(4).appendChild(document.createTextNode(userObj.ip_addr.toString()));
}

var addUsersToTable = async (response) => {
    let body = await response.json();
    body.forEach( el => {addRow("competitors", el)})
}


var updateUsersTable =  async () => {
    doGet("/competitors/", addUsersToTable);
};

updateUsersTable();


function what(form) {
    console.log("what")
    return false;
}


