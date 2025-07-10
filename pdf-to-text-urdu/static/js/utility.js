
function showPreview() {
    const fileInput = document.getElementById("fileInput");
    const previewContainer = document.getElementById("imagePreview");

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            // Create an image element or update an existing one
            let img = previewContainer.querySelector("img");
            if (!img) {
                img = document.createElement("img");
                previewContainer.innerHTML = ""; // Clear previous content
                previewContainer.appendChild(img);
            }
            img.src = e.target.result;
            previewContainer.style.display = "flex"; // Show the preview container
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}


async function extractText() {
    const fileInput = document.getElementById('fileInput');
    const responseMessage = document.getElementById('responseMessage');
    const rightLoader = document.getElementById('rightLoader');
    const submitButton = document.getElementById('submitButton');

    removeDownloadButton()

    responseMessage.innerHTML = ''; // Clear previous responses
    submitButton.disabled = true; // Disable button
    rightLoader.style.display = 'block';

    if (fileInput.files.length === 0) {
        alert('Please choose a file first.');
        rightLoader.style.display = 'none';
        submitButton.disabled = false;
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const url = `${window.location.origin}/api/perform_ocr`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        rightLoader.style.display = 'none';
        submitButton.disabled = false;

        if (result.predicted_data) {
//            responseMessage.innerHTML = `<h2>File: ${result.file}</h2>`;

            let pageNumber = 1;  // Initialize page number
            console.log(result.predicted_data)

            for (const [page, lines] of Object.entries(result.predicted_data)) {
                // Update the page heading to "Page #X"
                responseMessage.innerHTML += `<h3>Page #${pageNumber}</h3>`;

                // Increment the page number for the next page
                pageNumber++;

                for (const [line, text] of Object.entries(lines)) {
                    responseMessage.innerHTML += `<p class="result-text" >${text}</p>`;
                }
            }
        } else if (result.predicted_text) {
//            responseMessage.innerHTML = `<h2 style="font-size:15px;">File: ${result.file}</h2>`;
//            responseMessage.innerHTML += `<h3  style="font-family: 'nafees-nastaleeq'; font-size:17px;"><strong>Predicted Text:</strong></h3>`;
            Object.keys(result.predicted_text).forEach((lineKey) => {
                responseMessage.innerHTML += `<p class="result-text" >${result.predicted_text[lineKey]}</p>`;
            });
        } else {
            responseMessage.innerText = 'No text found.';
            return;
        }

        // Add Download Text button
        addDownloadButton();
    } catch (error) {
        console.error('Error:', error);
        rightLoader.style.display = 'none';
        submitButton.disabled = false;
        responseMessage.innerText = 'Failed to extract text. Please try again.';
    }
}


function addDownloadButton() {
    const responseMessage = document.getElementById('predicted-div');

    // Check if the button already exists to avoid duplication
    if (document.getElementById('downloadButton')) {
        return;
    }

    // Create the Download Text button
    const downloadButton = document.createElement('button');
    downloadButton.id = 'downloadButton'; // Add an ID to identify the button
    downloadButton.title = 'Download Text'; // Tooltip for clarity
    downloadButton.style.cssText = `
        margin-bottom: 10px;
        position: absolute;
        right: 10px;
        top: 10px;
        background: none;
        border: none;
        cursor: pointer;
        font-size: 24px;
        color: #007bff; /* Change color if needed */
    `;
    downloadButton.innerHTML = `<i class="fa-solid fa-download" style="color: blue;"></i>`; // Font Awesome icon
    downloadButton.onclick = downloadExtractedText;

    responseMessage.style.position = 'relative'; // Ensure the container can position elements
    responseMessage.insertBefore(downloadButton, responseMessage.firstChild);
}


function removeDownloadButton() {
    const downloadButton = document.getElementById('downloadButton');

    if (downloadButton) {
        downloadButton.remove(); // Remove the button from the DOM
    }
}


function downloadExtractedText() {
    let extractedText = '';

    // Select the response container
    const responseContainer = document.querySelector('#responseMessage');
    if (!responseContainer) {
        alert("No extracted text found!");
        return;
    }

    // Extract file name from <h2> if available
    const fileName = responseContainer.querySelector('h2')?.innerText?.split(':')[1]?.trim() || 'extracted_text';
    const sanitizedFileName = fileName.replace(/[^\w\d_-]/g, '_'); // Sanitize filename

    // Collect text in the order elements appear
    responseContainer.childNodes.forEach(element => {
        if (element.nodeType === Node.ELEMENT_NODE) { // Only process HTML elements
            if (element.matches('h1, h2, h3, h4, h5, h6')) {
                extractedText += element.innerText.trim() + '\n\n';
            } else if (element.matches('p.result-text')) {
                extractedText += element.innerText.trim() + '\n';
            }
        }
    });

    if (!extractedText.trim()) {
        alert("No text found to download!");
        return;
    }

    // Create a Blob for the extracted text
    const blob = new Blob([extractedText], { type: 'text/plain' });

    // Create a link element and trigger the download
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `extracted_text_${sanitizedFileName}.txt`;
    document.body.appendChild(link); // Append to the DOM to ensure it works in all browsers
    link.click();
    document.body.removeChild(link); // Clean up the DOM
}

