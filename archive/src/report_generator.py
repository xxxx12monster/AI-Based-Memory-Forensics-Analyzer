"""
AI Memory Forensics Report Generator
Generates comprehensive PDF reports for forensic analysis results.
"""

import os
from datetime import datetime
from io import BytesIO
import base64

class ForensicsReportGenerator:
    """Generates PDF-style HTML reports for memory forensics analysis."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
    def generate_report(self, scan_results, filename="forensic_report.html"):
        """
        Generate a comprehensive forensics report.
        
        Args:
            scan_results: List of dicts containing scan results per sample
            filename: Output filename for the report
            
        Returns:
            HTML content string and report path
        """
        # Calculate summary statistics
        total_samples = len(scan_results)
        malware_count = sum(1 for r in scan_results if r.get('status') == 'Malware')
        benign_count = total_samples - malware_count
        threat_level = self._calculate_threat_level(malware_count, total_samples)
        
        # Get malware type distribution
        malware_types = {}
        for r in scan_results:
            if r.get('status') == 'Malware':
                mal_type = r.get('type', 'Unknown')
                malware_types[mal_type] = malware_types.get(mal_type, 0) + 1
        
        # Build HTML report
        html_content = self._build_html_report(
            total_samples=total_samples,
            malware_count=malware_count,
            benign_count=benign_count,
            threat_level=threat_level,
            malware_types=malware_types,
            scan_results=scan_results
        )
        
        return html_content, self.report_id
    
    def _calculate_threat_level(self, malware_count, total):
        """Calculate overall threat level based on malware ratio."""
        if total == 0:
            return "UNKNOWN", "#888888"
        ratio = malware_count / total
        if ratio == 0:
            return "SECURE", "#00f260"
        elif ratio < 0.25:
            return "LOW", "#ffc107"
        elif ratio < 0.5:
            return "MEDIUM", "#ff9800"
        elif ratio < 0.75:
            return "HIGH", "#ff5722"
        else:
            return "CRITICAL", "#f44336"
    
    def _build_html_report(self, total_samples, malware_count, benign_count, 
                           threat_level, malware_types, scan_results):
        """Build the HTML report content."""
        
        threat_text, threat_color = threat_level
        
        # Build malware breakdown table
        malware_breakdown = ""
        for mal_type, count in sorted(malware_types.items(), key=lambda x: -x[1]):
            malware_breakdown += f"""
            <tr>
                <td>{mal_type}</td>
                <td>{count}</td>
                <td>{count/malware_count*100:.1f}%</td>
            </tr>
            """ if malware_count > 0 else ""
        
        # Build detailed results table
        detailed_results = ""
        for i, result in enumerate(scan_results[:100]):  # Limit to first 100 for report
            status_class = "malware" if result.get('status') == 'Malware' else "benign"
            anomaly_flag = "⚠️" if result.get('anomaly_score', 0) < 0 else ""
            detailed_results += f"""
            <tr class="{status_class}">
                <td>{i}</td>
                <td><span class="status-{status_class}">{result.get('status', 'Unknown')}</span></td>
                <td>{result.get('type', 'N/A')}</td>
                <td>{result.get('confidence', 0):.1f}%</td>
                <td>{result.get('anomaly_score', 0):.4f} {anomaly_flag}</td>
            </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memory Forensics Report - {self.report_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 40px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .header h1 {{
            color: #00f260;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 242, 96, 0.5);
        }}
        
        .header .subtitle {{
            color: #aaa;
            font-size: 1.1em;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .section h2 {{
            color: #0575E6;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(5, 117, 230, 0.3);
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.08);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .metric-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #00f260;
        }}
        
        .metric-card .label {{
            color: #aaa;
            margin-top: 5px;
        }}
        
        .threat-indicator {{
            font-size: 2em;
            font-weight: bold;
            color: {threat_color};
            text-shadow: 0 0 15px {threat_color};
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        th {{
            background: rgba(0, 242, 96, 0.1);
            color: #00f260;
            font-weight: 600;
        }}
        
        tr:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .status-malware {{
            color: #ff4b1f;
            font-weight: bold;
            background: rgba(255, 75, 31, 0.2);
            padding: 4px 12px;
            border-radius: 20px;
        }}
        
        .status-benign {{
            color: #00f260;
            font-weight: bold;
            background: rgba(0, 242, 96, 0.2);
            padding: 4px 12px;
            border-radius: 20px;
        }}
        
        .recommendations {{
            background: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin-top: 20px;
            border-radius: 0 10px 10px 0;
        }}
        
        .recommendations h3 {{
            color: #ffc107;
            margin-bottom: 15px;
        }}
        
        .recommendations ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .recommendations li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}
        
        .recommendations li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #ffc107;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            .section {{
                background: #f5f5f5;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Memory Forensics Analysis Report</h1>
            <p class="subtitle">CyberSentinel AI - Report ID: {self.report_id}</p>
            <p class="subtitle">Generated: {self.timestamp}</p>
        </div>
        
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="value">{total_samples}</div>
                    <div class="label">Total Samples</div>
                </div>
                <div class="metric-card">
                    <div class="value" style="color: #00f260;">{benign_count}</div>
                    <div class="label">Benign</div>
                </div>
                <div class="metric-card">
                    <div class="value" style="color: #ff4b1f;">{malware_count}</div>
                    <div class="label">Malware Detected</div>
                </div>
                <div class="metric-card">
                    <div class="threat-indicator">{threat_text}</div>
                    <div class="label">Threat Level</div>
                </div>
            </div>
        </div>
        
        {"<div class='section'><h2>🦠 Malware Type Distribution</h2><table><tr><th>Malware Family</th><th>Count</th><th>Percentage</th></tr>" + malware_breakdown + "</table></div>" if malware_count > 0 else ""}
        
        <div class="section">
            <h2>📋 Detailed Scan Results</h2>
            <table>
                <tr>
                    <th>Sample #</th>
                    <th>Classification</th>
                    <th>Malware Type</th>
                    <th>Confidence</th>
                    <th>Anomaly Score</th>
                </tr>
                {detailed_results}
            </table>
            {"<p style='color: #888; margin-top: 15px;'>Showing first 100 results. Total: " + str(total_samples) + "</p>" if total_samples > 100 else ""}
        </div>
        
        <div class="section">
            <h2>💡 Recommendations</h2>
            <div class="recommendations">
                <h3>Security Actions</h3>
                <ul>
                    {"<li>CRITICAL: Immediately isolate affected systems and begin incident response procedures.</li>" if threat_text == "CRITICAL" else ""}
                    {"<li>HIGH PRIORITY: Quarantine detected malware samples and conduct deep forensic analysis.</li>" if malware_count > 0 else ""}
                    {"<li>Review processes flagged with negative anomaly scores for potential zero-day threats.</li>" if any(r.get('anomaly_score', 0) < 0 for r in scan_results) else ""}
                    <li>Update endpoint protection signatures with detected malware indicators.</li>
                    <li>Document findings and update security incident log.</li>
                    {"<li>All systems appear clean. Continue regular monitoring.</li>" if malware_count == 0 else ""}
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>🛡️ CyberSentinel AI - AI-Powered Memory Forensics Analysis</p>
            <p>This report was automatically generated. For detailed analysis, consult with security professionals.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def get_download_link(self, html_content, filename="forensic_report.html"):
        """Generate a download link for the HTML report."""
        b64 = base64.b64encode(html_content.encode()).decode()
        return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display: inline-block; padding: 12px 24px; background: linear-gradient(90deg, #00f260, #0575E6); color: white; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 15px;">📥 Download Report</a>'


if __name__ == "__main__":
    # Test
    test_results = [
        {"status": "Malware", "type": "Ransomware", "confidence": 98.5, "anomaly_score": -0.23},
        {"status": "Benign", "type": "N/A", "confidence": 99.1, "anomaly_score": 0.12},
        {"status": "Malware", "type": "Spyware", "confidence": 87.2, "anomaly_score": -0.45},
    ]
    
    gen = ForensicsReportGenerator()
    html, report_id = gen.generate_report(test_results)
    
    with open(f"test_report_{report_id}.html", "w") as f:
        f.write(html)
    print(f"Test report generated: test_report_{report_id}.html")
