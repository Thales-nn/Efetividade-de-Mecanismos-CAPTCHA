const dashboardData = window.dashboardData || {
  bot: {
    total: 0,
    tempoMedio: 0,
    taxaEvasao: 0,
    taxaBloqueio: 0,
    valores: []
  },
  human: {
    total: 0,
    tempoMedio: 0,
    taxaSucessoHumano: 0,
    taxaErroHumano: 0,
    valores: []
  },
  iec: {
    valor: 0,
    seguranca: 0,
    usabilidade: 0,
    eficiencia: 0
  }
};

const formatSeconds = (value) => `${Number(value).toFixed(2)} s`;
const formatPercent = (value) => `${Number(value).toFixed(2)}%`;

function buildCharts() {
  const { bot, human } = dashboardData;

  new Chart(document.getElementById('botChart'), {
    type: 'line',
    data: {
      labels: Array.from({ length: bot.valores.length }, (_, i) => `#${i + 1}`),
      datasets: [{
        label: 'BOT',
        data: bot.valores,
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.14)',
        borderWidth: 2,
        fill: true,
        tension: 0.35,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: false },
        x: { ticks: { autoSkip: true, maxTicksLimit: 12 } }
      }
    }
  });

  new Chart(document.getElementById('humanosChart'), {
    type: 'line',
    data: {
      labels: Array.from({ length: human.valores.length }, (_, i) => `#${i + 1}`),
      datasets: [{
        label: 'Humanos',
        data: human.valores,
        borderColor: '#16a34a',
        backgroundColor: 'rgba(22, 163, 74, 0.12)',
        borderWidth: 2,
        fill: true,
        tension: 0.35,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: false },
        x: { ticks: { autoSkip: true, maxTicksLimit: 12 } }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', buildCharts);

window.addEventListener('load', () => {
  const { bot, human, iec } = dashboardData;

  const botEvasion = document.querySelector('[data-bot-evasion]');
  const botBlocking = document.querySelector('[data-bot-blocking]');
  const humanSuccess = document.querySelector('[data-human-success]');
  const humanError = document.querySelector('[data-human-error]');
  const botTempo = document.querySelector('[data-bot-time]');
  const humanTempo = document.querySelector('[data-human-time]');
  const iecValue = document.querySelector('[data-iec-value]');
  const iecSecurity = document.querySelector('[data-iec-security]');
  const iecUsability = document.querySelector('[data-iec-usability]');
  const iecEfficiency = document.querySelector('[data-iec-efficiency]');

  if (botEvasion) botEvasion.textContent = formatPercent(bot.taxaEvasao);
  if (botBlocking) botBlocking.textContent = formatPercent(bot.taxaBloqueio);
  if (humanSuccess) humanSuccess.textContent = formatPercent(human.taxaSucessoHumano);
  if (humanError) humanError.textContent = formatPercent(human.taxaErroHumano);
  if (botTempo) botTempo.textContent = formatSeconds(bot.tempoMedio);
  if (humanTempo) humanTempo.textContent = formatSeconds(human.tempoMedio);
  if (iecValue) iecValue.textContent = `${Number(iec.valor).toFixed(2)} / 100`;
  if (iecSecurity) iecSecurity.textContent = formatPercent(iec.seguranca);
  if (iecUsability) iecUsability.textContent = formatPercent(iec.usabilidade);
  if (iecEfficiency) iecEfficiency.textContent = formatPercent(iec.eficiencia);
});
