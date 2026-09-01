import json
import statistics
from pathlib import Path


BOT_TIMES = [
    2.10, 3.20, 3.80, 4.40, 4.90, 5.10, 5.30, 5.70, 6.00, 6.40,
    3.50, 4.70, 5.00, 5.60, 6.20, 7.30, 2.80, 4.20, 5.50, 5.90,
    6.70, 4.10, 4.50, 5.80, 6.90, 8.20, 3.60, 4.80, 5.40, 6.10,
]

HUMAN_TIMES = [
    4.10, 4.80, 5.20, 5.90, 6.40, 7.20, 7.80, 8.10, 8.90, 9.40,
    5.30, 6.00, 6.60, 7.10, 7.90, 8.40, 9.10, 9.80, 10.30, 11.10,
    5.70, 6.80, 7.30, 8.20, 8.70, 9.60, 12.10, 6.90, 7.50, 9.20,
]


def metricas(items):
    total = len(items)
    acertos = sum(1 for item in items if item["resultado"] == "SUCESSO")
    erros = sum(1 for item in items if item["resultado"] == "ERRO")
    tempos = [item["tempo_seg"] for item in items]
    media = statistics.mean(tempos) if tempos else 0
    taxa_bloqueio = (erros / total * 100) if total else 0
    taxa_acerto = (acertos / total * 100) if total else 0

    return {
        "total": total,
        "acertos": acertos,
        "erros": erros,
        "tempo_total": round(sum(tempos), 2),
        "tempo_medio": round(media, 2),
        "taxa_bloqueio": round(taxa_bloqueio, 2),
        "taxa_acerto": round(taxa_acerto, 2),
    }


def calcular_iec(bot_metrics, humanos_metrics):
    seguranca = 100 - bot_metrics["taxa_acerto"]
    usabilidade = humanos_metrics["taxa_acerto"]
    eficiencia = max(0, min(100, (16 - humanos_metrics["tempo_medio"]) / 16 * 100))
    indice = (seguranca + usabilidade + eficiencia) / 3
    return {
        "valor": round(indice, 2),
        "seguranca": round(seguranca, 2),
        "usabilidade": round(usabilidade, 2),
        "eficiencia": round(eficiencia, 2),
    }


def montar_dados(nome, tempos, acertos):
    dados = []
    for idx, tempo in enumerate(tempos, start=1):
        resultado = "SUCESSO" if idx <= acertos else "ERRO"
        dados.append({
            "tentativa": idx,
            "tempo_seg": tempo,
            "resultado": resultado,
        })
    return dados


BOT = montar_dados("BOT", BOT_TIMES, 25)
HUMANOS = montar_dados("Humanos", HUMAN_TIMES, 23)

BOT_METRICS = metricas(BOT)
HUMANOS_METRICS = metricas(HUMANOS)
IEC_METRICS = calcular_iec(BOT_METRICS, HUMANOS_METRICS)


def format_pct(value):
    return f"{value:.2f}%"


def format_seg(value):
    return f"{value:.2f} s"


def build_chart_dataset(label, values):
    values_str = ", ".join(f"{v:.2f}" for v in values)
    return f"{{ label: '{label}', data: [{values_str}], borderColor: '#2563eb', backgroundColor: 'rgba(37, 99, 235, 0.12)', borderWidth: 2, fill: false, tension: 0.35, pointRadius: 4 }}"


html_doc = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Análise CAPTCHA - TCC</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="styles.css" />
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="eyebrow">TCC · Análise de efetividade</div>
            <h1>CAPTCHA: BOT × Usuários Humanos</h1>
            <div class="subtitle">Comparativo do tempo de resolução, taxa de evasão, bloqueio e desempenho entre agentes automatizados e participantes humanos.</div>
        </div>

        <div class="cards">
            <div class="card green">
                <small>Humanos — total</small>
                <strong>{HUMANOS_METRICS['total']}</strong>
            </div>
            <div class="card orange">
                <small>Taxa de sucesso — Humanos</small>
                <strong>{format_pct(HUMANOS_METRICS['taxa_acerto'])}</strong>
            </div>
            <div class="card green">
                <small>Tempo médio — Humanos</small>
                <strong>{format_seg(HUMANOS_METRICS['tempo_medio'])}</strong>
            </div>

            <div class="card blue">
                <small>BOT — total</small>
                <strong>{BOT_METRICS['total']}</strong>
            </div>
            <div class="card blue">
                <small>Taxa de evasão — BOT</small>
                <strong>{format_pct(BOT_METRICS['taxa_acerto'])}</strong>
            </div>
            <div class="card blue">
                <small>Tempo médio — BOT</small>
                <strong>{format_seg(BOT_METRICS['tempo_medio'])}</strong>
            </div>
        </div>

        <div class="panel">
            <h2>Resumo executivo</h2>
            <div class="summary">
                O grupo humano exigiu <strong>{format_seg(HUMANOS_METRICS['tempo_medio'])}</strong> em média para resolver o CAPTCHA, enquanto o BOT respondeu em <strong>{format_seg(BOT_METRICS['tempo_medio'])}</strong>. A taxa de evasão do BOT foi de <strong>{format_pct(BOT_METRICS['taxa_acerto'])}</strong>, enquanto a taxa de sucesso humano foi de <strong>{format_pct(HUMANOS_METRICS['taxa_acerto'])}</strong>.
                <br><br>
                Esses resultados demonstram que o CAPTCHA apresenta respostas diferentes entre agentes automatizados e usuários humanos, sendo mais rápido para bots e mais consistente em termos de comportamento humano.
            </div>
        </div>

        <div class="panel">
            <h2>Métricas comparativas</h2>
            <table>
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>BOT</th>
                        <th>Humanos</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Taxa de Evasão</td><td>{format_pct(BOT_METRICS['taxa_acerto'])}</td><td>—</td></tr>
                    <tr><td>Taxa de Bloqueio</td><td>{format_pct(BOT_METRICS['taxa_bloqueio'])}</td><td>—</td></tr>
                    <tr><td>Taxa de Sucesso Humano</td><td>—</td><td>{format_pct(HUMANOS_METRICS['taxa_acerto'])}</td></tr>
                    <tr><td>Taxa de Erro Humano</td><td>—</td><td>{format_pct(HUMANOS_METRICS['taxa_bloqueio'])}</td></tr>
                    <tr><td>Tempo Médio de Resolução</td><td>{format_seg(BOT_METRICS['tempo_medio'])}</td><td>{format_seg(HUMANOS_METRICS['tempo_medio'])}</td></tr>
                </tbody>
            </table>
        </div>

        <div class="panel">
            <h2>Fórmulas da análise</h2>
            <div class="summary">
                <p><strong>Taxa de Evasão:</strong> TE = (sucessos dos bots / tentativas dos bots) × 100</p>
                <p><strong>Taxa de Bloqueio:</strong> TB = (erros dos bots / tentativas dos bots) × 100</p>
                <p><strong>Taxa de Sucesso Humano:</strong> TSH = (sucessos humanos / tentativas humanas) × 100</p>
                <p><strong>Taxa de Erro Humano:</strong> TEH = (erros humanos / tentativas humanas) × 100</p>
                <p><strong>Tempo Médio de Resolução:</strong> TMR = (somatório dos tempos / número de tentativas)</p>
            </div>
        </div>

        <div class="panel">
            <h2>Índice de Efetividade CAPTCHA (IEC)</h2>
            <div class="iec-container">
                <div class="iec-card">
                    <span class="badge">Resultado geral</span>
                    <div class="iec-value">{IEC_METRICS['valor']:.2f} / 100</div>
                    <div class="component">
                        <span>Segurança</span>
                        <strong>{IEC_METRICS['seguranca']:.2f}%</strong>
                    </div>
                    <div class="component">
                        <span>Usabilidade</span>
                        <strong>{IEC_METRICS['usabilidade']:.2f}%</strong>
                    </div>
                    <div class="component">
                        <span>Eficiência temporal</span>
                        <strong>{IEC_METRICS['eficiencia']:.2f}%</strong>
                    </div>
                </div>

                <div class="iec-card methodology">
                    <h3>Metodologia do IEC</h3>
                    <p>O Índice de Efetividade CAPTCHA (IEC) sintetiza três componentes: segurança, usabilidade e eficiência temporal.</p>
                    <p><strong>Segurança:</strong> 1 − taxa de sucesso do BOT.</p>
                    <p><strong>Usabilidade:</strong> taxa de sucesso dos usuários humanos.</p>
                    <p><strong>Eficiência:</strong> baseada no tempo médio humano, utilizando 16 segundos como referência.</p>
                    <p>Os três componentes possuem o mesmo peso no índice.</p>
                </div>
            </div>
        </div>

        <div class="charts">
            <div class="panel">
                <h2>Tempo por tentativa — BOT</h2>
                <div class="chart-box">
                    <canvas id="botChart"></canvas>
                </div>
            </div>
            <div class="panel">
                <h2>Tempo por tentativa — Humanos</h2>
                <div class="chart-box">
                    <canvas id="humanosChart"></canvas>
                </div>
            </div>
        </div>

        <div class="panel">
            <h2>Resultados gerais</h2>
            <table>
                <thead>
                    <tr>
                        <th>Resultado</th>
                        <th>BOT</th>
                        <th>Humanos</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Total de tentativas</td><td>{BOT_METRICS['total']}</td><td>{HUMANOS_METRICS['total']}</td></tr>
                    <tr><td>Acertos</td><td>{BOT_METRICS['acertos']}</td><td>{HUMANOS_METRICS['acertos']}</td></tr>
                    <tr><td>Erros</td><td>{BOT_METRICS['erros']}</td><td>{HUMANOS_METRICS['erros']}</td></tr>
                    <tr><td>Tempo total</td><td>{format_seg(BOT_METRICS['tempo_total'])}</td><td>{format_seg(HUMANOS_METRICS['tempo_total'])}</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        window.dashboardData = {json.dumps({
            "bot": {
                "total": BOT_METRICS['total'],
                "tempoMedio": BOT_METRICS['tempo_medio'],
                "taxaEvasao": BOT_METRICS['taxa_acerto'],
                "taxaBloqueio": BOT_METRICS['taxa_bloqueio'],
                "valores": [item['tempo_seg'] for item in BOT],
                "acertos": BOT_METRICS['acertos'],
                "erros": BOT_METRICS['erros']
            },
            "human": {
                "total": HUMANOS_METRICS['total'],
                "tempoMedio": HUMANOS_METRICS['tempo_medio'],
                "taxaSucessoHumano": HUMANOS_METRICS['taxa_acerto'],
                "taxaErroHumano": HUMANOS_METRICS['taxa_bloqueio'],
                "valores": [item['tempo_seg'] for item in HUMANOS],
                "acertos": HUMANOS_METRICS['acertos'],
                "erros": HUMANOS_METRICS['erros']
            },
            "iec": {
                "valor": IEC_METRICS['valor'],
                "seguranca": IEC_METRICS['seguranca'],
                "usabilidade": IEC_METRICS['usabilidade'],
                "eficiencia": IEC_METRICS['eficiencia']
            }
        }, ensure_ascii=False)};
    </script>
    <script src="script.js"></script>
</body>
</html>
"""

output_dir = Path(__file__).resolve().parent
output_file = output_dir / "dashboard.html"
output_file.write_text(html_doc, encoding="utf-8")
print(f"Dashboard gerado em: {output_file}")
print(f"BOT: {BOT_METRICS}")
print(f"Humanos: {HUMANOS_METRICS}")
print(f"IEC: {IEC_METRICS}")
