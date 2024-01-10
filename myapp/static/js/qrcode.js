url = new URL(document.URL)
qrcodeData = url.origin + `/store/${store_slug}/review`

options = {
  width: 150,
  height: 150,
  type: "svg",
  data: qrcodeData,
  dotsOptions: {
    color: "#be123c",
    type: "extra-rounded"
  },
  cornersSquareOptions: {
    type: "extra-rounded",
  },
  backgroundOptions: {
    color: "#fff",
  },
  imageOptions: {
    crossOrigin: "anonymous",
    margin: 20
  },
  qrOptions: {
    errorCorrectionLevel: 'H'
  }
};

document.querySelectorAll('.qrcode').forEach((element) => {
  qrCode = new QRCodeStyling(options);
  qrCode.append(element);
});


const downloadButtons = document.querySelectorAll('button');

html2canvas(document.querySelector("#poster-source")).then(canvas => {
  downloadButton = downloadButtons[0];
  downloadButton.parentElement.insertBefore(canvas, downloadButton);
  downloadButton.classList.remove('hidden');

  html2canvas(document.querySelector("#folded-poster-source")).then(canvas => {
    downloadButton = downloadButtons[1];
    downloadButton.parentElement.insertBefore(canvas, downloadButton);
    downloadButton.classList.remove('hidden');
    document.querySelector('#preload').remove();
  });
});


downloadButtons.forEach((button) => {
  button.onclick = (event) => {
    const canvas = event.target.parentElement.querySelector('canvas');
    let canvasUrl = canvas.toDataURL("image/jpeg", 1);
    console.log(canvasUrl);
    const createEl = document.createElement('a');
    createEl.href = canvasUrl;
    createEl.download = "poster.jpg";
    createEl.click();
    createEl.remove();
  }
});
