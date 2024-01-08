const couponCode = document.getElementById("coupon");
const validateButton = document.getElementById("validate");
const loader = document.querySelector(".loader");

const messagesContainer = document.createElement('div');
const main = document.getElementById('main');
main.prepend(messagesContainer);
const couponCard = document.createElement('div');
main.append(couponCard);

showCoupon = (coupon) => {
	const redeemURL = `/redeem/${coupon.code}`;
	const deleteURL = `/delete/${coupon.code}`;
	let datetime = moment.utc(coupon.expire_date).add(1, 'hours').format('MMMM DD, YYYY hh:mm:ss A') + ' CET';
	let badgeHTML = '<span class="rounded bg-green-100 px-2.5 py-0.5 text-xs font-medium uppercase tracking-wide text-green-800">Valid</span>';
	let actionHTML = `<div class="mt-2"><a href="${redeemURL}"><button class="primary px-3 py-2 text-xs uppercase">Redeem</button></a></div>`;
	
	if (moment.utc(coupon.expire_date) < moment.utc()) {
		badgeHTML = '<span class="rounded bg-red-100 px-2.5 py-0.5 text-xs font-medium uppercase tracking-wide text-red-800">Invalid</span>';
		actionHTML = `<div class="mt-2"><a href="${deleteURL}"><button class="text-white bg-rose-600 hover:bg-rose-800 px-3 py-2 text-xs uppercase">Delete</button></a></div>`;
	}
	
	couponCard.innerHTML = `<div class="m-4 w-fit max-w-[400px] rounded p-4 shadow shadow-gray-300">
  <div class="mb-2 flex items-center justify-between">
    <span class="font-bold tracking-wide">${coupon.code}</span>
    ${badgeHTML}
  </div>
  <div class="mt-1 text-sm">Expire Date</div>
	<div class="text-sm text-gray-600">${datetime}</div>
	<div class="mt-2 text-sm">Offer</div>
	<div class="text-sm text-gray-600">${coupon.offer}</div>
  ${actionHTML}
</div>`;
};

couponCode.onkeypress = (event) => {
	if (event.key === 'Enter') {
		validateButton.click();
	}
};

couponCode.oninput = () => {
	couponCode.value = couponCode.value.replace(' ', '').toUpperCase();
};

validateButton.onclick = () => {
	let coupon = couponCode.value.trim();
	if (coupon === '') {
    messageElem = document.createElement('div')
    messageElem.innerText = 'Empty coupon can not be validated';
    messageElem.classList.add('alert-error');
    messagesContainer.appendChild(messageElem);
	} else {
		loader.classList.remove("hidden");
		url = "/search_coupon/" + coupon;
		fetch(url)
			.then(resp => resp.json())
			.then((data) => {
				loader.classList.add("hidden");
				if(data.coupon) showCoupon(data.coupon);
				else {
    			messageElem = document.createElement('div')
    			messageElem.innerText = 'This coupon does not exist';
    			messageElem.classList.add('alert-error');
    			messagesContainer.appendChild(messageElem);
				}
			});
	}
  setTimeout(() => {
    messagesContainer.innerHTML = '';
  }, 3000);
};
