// Global variables for the JSON data and XHR objects
var jsonData1, jsonString1, xhr1;
var pageNumber = 0;
var pageTotal = 0;
let itemBarcode = [9], itemQuantity = [9], itemURL = [9];
let itemTags = [9][5];
var tag = "nothing";
var itemsPerPage = 9;


window.addEventListener('load', function() {
  // Create JSON data for the request on page load
  jsonData1 = {
    Start: pageNumber*9,
    End: (pageNumber + 1)*9,
    TotalTags: "True",
    TotalPages: "True",
    FilterBy: tag
  };

    // Convert JSON to string for the request on page load
    jsonString1 = JSON.stringify(jsonData1);

    // Create a new XMLHttpRequest object for the request on page load
    xhr1 = new XMLHttpRequest();
    xhr1.open('GET', '/store/Items', true);
    xhr1.setRequestHeader('Content-Type', 'application/json');
    xhr1.onreadystatechange = function() {
        if (xhr1.readyState === XMLHttpRequest.DONE && xhr1.status === 200) {
            var response1 = JSON.parse(xhr1.responseText);
            console.log(response1);
            pageTotal = response1.TotalPages;
            for (var i = 0; i < response1.Data.length; i++) {
                //replace
                itemBarcode[i] = response1.Data.Barcode[i];
                itemQuantity[i] = response1.Data.Quantity[i];
                itemURL[i] = response1.Data.iURL[i];
                for(var j = 0; j < response1.Data.Tags[i].length; j++){
                    itemTags[i][j] = response1.Data.Tags[i][j];
                }
            }
        }
    };
    xhr1.send(jsonString1);
});

var button = document.getElementById('prevButton');
button.addEventListener('click', function() {
    if(pageNumber > 0){
        // Create JSON data for the request on button click
        pageNumber -= 1;
        var jsonData2 = {
            Start: (pageNumber-1)*9,
            End: pageNumber*9,
            TotalTags: F,
            TotalPages: F,
            Filter: tag
        };

        // Convert JSON to string for the request on button click
        var jsonString2 = JSON.stringify(jsonData2);

        // Create a new XMLHttpRequest object for the request on button click
        var xhr2 = new XMLHttpRequest();
        xhr2.open('GET', '/store/Items', true);
        xhr2.setRequestHeader('Content-Type', 'application/json');
        xhr2.onreadystatechange = function() {
            if (xhr2.readyState === XMLHttpRequest.DONE && xhr2.status === 200) {
                var response2 = JSON.parse(xhr2.responseText);
                console.log(response2);
                for (var i = 0; i < response1.Data.length; i++) {
                    //replace
                    itemBarcode[i] = response1.Data.Barcode[i];
                    itemQuantity[i] = response1.Data.Quantity[i];
                    itemURL[i] = response1.Data.iURL[i];
                    for(var j = 0; j < response1.Data.Tags[i].length; j++){
                        itemTags[i][j] = response1.Data.Tags[i][j];
                    }
                }
                UpdateGrid();
            }
        };
        xhr2.send(jsonString2);
    }
});

var button = document.getElementById('nextButton');
button.addEventListener('click', function() {
    if(pageNumber < pageTotal){
        // Create JSON data for the request on button click
        pageNumber += 1;
        var jsonData3 = {
            Start: pageNumber*9,
            End: (pageNumber + 1)*9,
            TotalTags: F,
            TotalPages: F,
            FilterBy: tag
        };

        // Convert JSON to string for the request on button click
        var jsonString3 = JSON.stringify(jsonData3);

        // Create a new XMLHttpRequest object for the request on button click
        var xhr3 = new XMLHttpRequest();
        xhr3.open('GET', '/store/Items', true);
        xhr3.setRequestHeader('Content-Type', 'application/json');
        xhr3.onreadystatechange = function() {
            if (xhr3.readyState === XMLHttpRequest.DONE && xhr3.status === 200) {
                var response3 = JSON.parse(xhr3.responseText);
                console.log(response3);
                for (var i = 0; i < response1.Data.length; i++) {
                    //replace
                    itemBarcode[i] = response1.Data.Barcode[i];
                    itemQuantity[i] = response1.Data.Quantity[i];
                    itemURL[i] = response1.Data.iURL[i];
                    for(var j = 0; j < response1.Data.Tags[i].length; j++){
                        itemTags[i][j] = response1.Data.Tags[i][j];
                    }
                }
                UpdateGrid();
            }
        };
        xhr3.send(jsonString3);
    }
});

function UpdateGrid(){

    // Clear existing grid items
    gridContainer.innerHTML = '';

    // Create grid items dynamically based on the data
    for (var i = 0; i < itemsPerPage; i++) {
        var itemId = itemBarcode[i];
        var gridItem = document.createElement('div');
        gridItem.className = 'grid-item';

        var image = document.createElement('img');
        image.src = itemURL[i];
        image.alt = 'Image';
        image.dataset.id = itemId; // Assign ID to the image

        image.addEventListener('click', function() {
            var itemId = this.dataset.id;
            console.log('Clicked Image ID:', itemId);
        });

        gridItem.appendChild(image);
        gridContainer.appendChild(gridItem);
    }
}
