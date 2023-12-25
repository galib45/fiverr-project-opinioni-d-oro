function getRandomRating(min = 3.5, max = 5) {
  return Math.random() * (max - min) + min;
}

function nextDate(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1);
}

fetch('/chartdata').then(resp => resp.json()).then((data) => {
  store_created = moment.unix(data.store_created).utc();
  total_elapsed_days = moment.duration(moment().diff(store_created)).get('days');
  ratings = Array(total_elapsed_days+1);
  averages = Array(total_elapsed_days+1);
  labels = Array(total_elapsed_days+1);
  
  for(update of data.updates) {
    review_updated = moment.unix(update.timestamp).utc();
    elapsed_days = moment.duration(review_updated.diff(store_created)).get('days');
    if (!ratings[elapsed_days]) ratings[elapsed_days] = [];
    ratings[elapsed_days].push(update.rating);
  }
  
  sum = 0; length = 0;
  for (i=0; i<=total_elapsed_days; i++) {
    if (ratings[i]) {
      sum += ratings[i].reduce((a,b)=>a+b);
      length += ratings[i].length;
    }
    averages[i] = sum/length;
    labels[i] = store_created.local().format('DD MMMM, YYYY');
    store_created.add(1, 'days');
  }

  chart = new Chart(document.getElementById("chart"), {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Average Rating",
          data: averages,
          borderWidth: 2,
          borderColor: "rgb(22 163 74)",
          borderCapStyle: "round",
          borderJoinStyle: "round",
          pointRadius: 4,
          pointBackgroundColor: "rgb(22 163 74)",
        },
      ],
    },
    options: {
      layout: {
        padding: 20,
      },
      scales: {
        x: {
          display: false,
        },
        y: {
          suggestedMin: 3,
          suggestedMax: 5,
          display: true,
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
});



