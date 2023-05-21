// Global variables for the JSON data and XHR objects
var jsonData1, jsonData2, jsonData3, jsonData4, jsonData5;
var jsonString1, jsonString2, jsonString3, jsonString4, jsonString5;
var xhr1, xhr2, xhr3, xhr4, xhr5;
var pageNumber = 0;
var pageTotal = 0;
let itemBarcode = [9], itemQuantity = [9], itemURL = [9];
let itemTags = [9][5];
let totalTags = [];
var itemLength;
var tag = "none";
var itemsPerPage = 9;
let ShoppingCart = [];
var tagVal;


window.addEventListener('load', function() {
  // Create JSON data for the request on page load
  jsonData1 = {
    Start: pageNumber*9,
    End: (pageNumber + 1)*9 -1,
    TotalTags: `true`,
    TotalPages: `true`,
    FilterBy: tag
  };

    // Convert JSON to string for the request on page load
    jsonString1 = JSON.stringify(jsonData1);

    // Create a new XMLHttpRequest object for the request on page load
    xhr1 = new XMLHttpRequest();
    xhr1.open('POST', 'http://127.0.0.1:5000/store/Items/get', true);
    xhr1.setRequestHeader('Content-Type', 'application/json');
    xhr1.onreadystatechange = function() {
        if (xhr1.readyState === XMLHttpRequest.DONE && xhr1.status === 200) {
            var response1 = JSON.parse(xhr1.responseText);
            console.log(response1);
            pageTotal = response1.TotalPages;
            itemLength = response1.Barcode.length;
            for (var i = 0; i < itemLength; i++) {
                //replace
                itemBarcode[i] = response1.Barcode[i];
                itemURL[i] = response1.imgURL[i];

                // for(var j = 0; j < 5; j++){
                //     itemTags[i][j] = response1.Tags[i][j];
                // }
            }

            for (var j = 0; j < response1.TotalTags; j++){
                totalTags[j] = response1.Tags[j];
            }

            UpdateGrid();
        }
    };
    console.log(jsonString1);
    
    xhr1.send(jsonString1);
});

var button = document.getElementById('prevButton');
button.addEventListener('click', function() {
    ListAll();

    if(pageNumber > 0){
        // Create JSON data for the request on button click
        pageNumber -= 1;
        jsonData2 = {
            Start: (pageNumber-1)*9,
            End: pageNumber*9,
            TotalTags: `false`,
            TotalPages: `false`,
            Filter: tag
        };

        // Convert JSON to string for the request on button click
        var jsonString2 = JSON.stringify(jsonData2);

        // Create a new XMLHttpRequest object for the request on button click
        var xhr2 = new XMLHttpRequest();
        xhr2.open('GET', 'http://127.0.0.1:5000/store/Items/get');
        xhr2.setRequestHeader('Content-Type', 'application/json');
        xhr2.onreadystatechange = function() {
            if (xhr2.readyState === XMLHttpRequest.DONE && xhr2.status === 200) {
                var response2 = JSON.parse(xhr2.responseText);
                console.log(response2);
                itemLength = response2.Barcode.length;
                for (var i = 0; i < itemLength; i++) {
                    //replace
                    itemBarcode[i] = response2.Barcode[i];
                    itemURL[i] = response2.imgURL[i];
                    // for(var j = 0; j < 5; j++){
                    //     itemTags[i][j] = response2.Tags[i][j];
                    // }
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
            TotalTags: `false`,
            TotalPages: `false`,
            FilterBy: tag
        };

        // Convert JSON to string for the request on button click
        var jsonString3 = JSON.stringify(jsonData3);

        // Create a new XMLHttpRequest object for the request on button click
        var xhr3 = new XMLHttpRequest();
        xhr3.open('GET', 'http://127.0.0.1:5000/store/Items/get');
        xhr3.setRequestHeader('Content-Type', 'application/json');
        xhr3.setRequestHeader('Content-Length', '96');
        
        xhr3.onreadystatechange = function() {
            if (xhr3.readyState === XMLHttpRequest.DONE && xhr3.status === 200) {
                var response3 = JSON.parse(xhr3.responseText);
                console.log(response3.imgURL);
                itemLength = response3.Barcode.length;
                for (var i = 0; i < itemLength; i++) {
                    //replace
                    itemBarcode[i] = response3.Barcode[i];
                    // itemQuantity[i] = response3.Quantity[i];
                    itemURL[i] = response3.imgURL[i];
                    // for(var j = 0; j < 5; j++){
                    //     itemTags[i][j] = response3.Tags[i][j];
                    // }
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
    for (var i = 0; i < itemLength; i++) {
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
            ShoppingCart.push("itemId");
            $('#itemId li a').css('color', 'blue');
        });

        gridItem.appendChild(image);
        gridContainer.appendChild(gridItem);
    }
}

var button = document.getElementById('order');
button.addEventListener('click', function() {
    if(pageNumber < pageTotal){
        // Create JSON data for the request on button click
        pageNumber += 1;
        var jsonData4 = {
            Order: ShoppingCart
        };

        // Convert JSON to string for the request on button click
        var jsonString4 = JSON.stringify(jsonData4);

        // Create a new XMLHttpRequest object for the request on button click
        var xhr4 = new XMLHttpRequest();
        xhr4.open('GET', 'http://127.0.0.1:5000/store/reserve');
        xhr4.setRequestHeader('Content-Type', 'application/json');
        xhr4.setRequestHeader('Content-Length', '96');
        
        xhr4.onreadystatechange = function() {
            if (xhr4.readyState === XMLHttpRequest.DONE && xhr4.status === 200) {
                var response4 = JSON.parse(xhr4.responseText);
                console.log(response4.imgURL);
                for (var i = 0; i < itemLength; i++) {
                    //replace
                    itemBarcode[i] = response4.Barcode[i];
                    itemURL[i] = response4.imgURL[i];
    
                    // for(var j = 0; j < 5; j++){
                    //     itemTags[i][j] = response1.Tags[i][j];
                    // }
                }
            }
        };
        xhr4.send(jsonString4);
    }
});

function ListAll() {
    var select = document.getElementById("filterTag");
    for (var i = 0; i < totalTags.length; i++) {
        var opt = totalTags[i];
        var ls = document.createElement("option");
        ls.textContent = opt;
        ls.value = opt;
        select.appendChild(totalTags[ls]);
    }
}

var button = document.getElementById('filter');
button.addEventListener('click', function() {
    var tag = document.getElementById("filterTag").value;

    jsonData5 = {
        Start: pageNumber*9,
        End: (pageNumber + 1)*9 -1,
        TotalTags: `true`,
        TotalPages: `true`,
        FilterBy: tag
    };

    // Convert JSON to string for the request on button click
    var jsonString5 = JSON.stringify(jsonData5);

    // Create a new XMLHttpRequest object for the request on button click
    var xhr5 = new XMLHttpRequest();
    xhr5.open('GET', 'http://127.0.0.1:5000/items/get');
    xhr5.setRequestHeader('Content-Type', 'application/json');
    xhr5.setRequestHeader('Content-Length', '96');
    
    xhr5.onreadystatechange = function() {
        if (xhr5.readyState === XMLHttpRequest.DONE && xhr5.status === 200) {
            var response5 = JSON.parse(xhr5.responseText);
            console.log(response5.imgURL);
            for (var i = 0; i < itemLength; i++) {
                itemBarcode[i] = response5.Barcode[i];
                itemURL[i] = response5.imgURL[i];
            }
        }
    };
    xhr5.send(jsonString5);
});