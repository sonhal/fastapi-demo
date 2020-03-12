

var doPost = (payload, path) => {
    const request = new Request('http://localhost:8000' + path, {method: 'POST', body: JSON.stringify(payload)});
        fetch(request).then(response => {
    if (response.status === 200) {
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
    const request = new Request('http://localhost:8000' + path, {method: 'GET'});
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
        age: parseInt(formData.get("age").toString())
    };

    console.log( payload );
    doPost(payload, "/users/");
    updateUsersTable();
    return false; //don't submit
};

function addRow(tableID, userObj) {
  // Get a reference to the table
  let tableRef = document.getElementById(tableID);
  if(tableRef.rows.length -1> userObj.id) return; // Already in table
    console.log(tableRef.rows )

  // Insert a row at the end of the table
  let newRow = tableRef.insertRow(-1);

  Object.values(userObj).forEach( (el, i) => {
      let newCell = newRow.insertCell(i);
      let newText = document.createTextNode(el.toString());
      newCell.appendChild(newText);
  });
}

var addUsersToTable = async (response) => {
    let body = await response.json();
    body.forEach( el => {addRow("users", el)})
}


var updateUsersTable =  async () => {
    doGet("/users", addUsersToTable);
};

updateUsersTable();



