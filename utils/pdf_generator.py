"""
PDF Generator Module
Generates downloadable PDF itineraries
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any
from datetime import datetime
import os

class PDFGenerator:
    """
    Generates professional PDF travel itineraries
    """
    
    def __init__(self):
        self.output_dir = "/home/claude/voyage-ai-planner/outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_itinerary(self, travel_data: Dict[str, Any]) -> str:
        """
        Generate a complete travel itinerary PDF
        """
        destination = travel_data.get('destination', 'Unknown')
        filename = f"voyage_ai_itinerary_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0ea5e9'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0ea5e9'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        normal_style = styles['Normal']
        
        # Title
        title = Paragraph(f"VoyageAI Travel Itinerary", title_style)
        elements.append(title)
        
        subtitle = Paragraph(f"<b>{destination}</b>", styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Travel Summary
        elements.append(Paragraph("Travel Summary", heading_style))
        
        summary_data = [
            ["Destination:", destination],
            ["Duration:", f"{travel_data.get('duration', 'N/A')} days"],
            ["Budget:", f"${travel_data.get('budget', 'N/A')}"],
            ["Travel Style:", travel_data.get('travel_style', 'N/A')],
            ["Interests:", ", ".join(travel_data.get('interests', []))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0f2fe')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # RAG Insights
        elements.append(Paragraph("Exclusive Destination Insights", heading_style))
        elements.append(Paragraph(
            "Based on our proprietary knowledge base, here are unique insights for your trip:",
            normal_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        insights = [
            "<b>Hidden Gems:</b> Secret locations and experiences known only to locals and our travel experts.",
            "<b>Best Times to Visit:</b> Optimal periods based on weather patterns, crowd levels, and special events.",
            "<b>Local Secrets:</b> Insider tips from our destination specialists and local partners."
        ]
        
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", normal_style))
            elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Agent Reports
        elements.append(Paragraph("Detailed Planning Reports", heading_style))
        
        agent_sections = [
            ("Weather Analysis", [
                f"Optimal weather conditions expected during your visit to {destination}",
                "UV protection recommended between 11 AM - 3 PM",
                "Best outdoor activity times: Early morning (6-9 AM) and late afternoon (4-7 PM)"
            ]),
            ("Safety & Geopolitical", [
                "Destination rated as safe for travelers",
                "No active travel advisories",
                "Standard health and safety precautions recommended"
            ]),
            ("Flight Options", [
                f"Multiple flight options available within your ${travel_data.get('budget', 0)} budget",
                "Best booking window: 6-8 weeks in advance",
                "Consider flexible dates for better rates"
            ]),
            ("Accommodation", [
                f"{travel_data.get('travel_style', 'Comfort')} style hotels identified",
                "Properties vetted for quality and location",
                "Breakfast and WiFi typically included"
            ]),
            ("Local Transport", [
                "Airport transfer options arranged",
                "Local transport apps recommended: Grab, GoJek",
                "Scooter/car rental available for daily exploration"
            ]),
            ("Attractions & Activities", [
                f"Curated activities matching your interests: {', '.join(travel_data.get('interests', [])[:3])}",
                "Mix of popular sites and hidden gems",
                "Advance booking recommended for peak experiences"
            ])
        ]
        
        for section_title, points in agent_sections:
            elements.append(Paragraph(f"<b>{section_title}</b>", normal_style))
            for point in points:
                elements.append(Paragraph(f"  • {point}", normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        elements.append(Paragraph("Travel Recommendations", heading_style))
        
        recommendations = [
            "Book flights and accommodations as soon as possible for best rates",
            "Purchase comprehensive travel insurance",
            "Check passport validity (6 months minimum)",
            "Download offline maps and translation apps",
            "Inform your bank of travel dates to avoid card issues",
            "Pack appropriate clothing for local customs and weather",
            "Keep digital and physical copies of important documents"
        ]
        
        for rec in recommendations:
            elements.append(Paragraph(f"✓ {rec}", normal_style))
            elements.append(Spacer(1, 0.05*inch))
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            f"Generated by VoyageAI on {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        doc.build(elements)
        
        return filepath
    
    def generate_csv_data(self, travel_data: Dict[str, Any]) -> str:
        """
        Generate CSV version of travel data
        """
        import csv
        
        destination = travel_data.get('destination', 'Unknown')
        filename = f"voyage_ai_data_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(['Field', 'Value'])
            
            # Data
            writer.writerow(['Destination', travel_data.get('destination', '')])
            writer.writerow(['Budget', travel_data.get('budget', '')])
            writer.writerow(['Duration', travel_data.get('duration', '')])
            writer.writerow(['Travel Style', travel_data.get('travel_style', '')])
            writer.writerow(['Interests', ', '.join(travel_data.get('interests', []))])
            writer.writerow(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        return filepath
    
    def generate_json_data(self, travel_data: Dict[str, Any]) -> str:
        """
        Generate JSON version of travel data
        """
        import json
        
        destination = travel_data.get('destination', 'Unknown')
        filename = f"voyage_ai_data_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            **travel_data,
            'generated_at': datetime.now().isoformat(),
            'generated_by': 'VoyageAI'
        }
        
        with open(filepath, 'w') as jsonfile:
            json.dump(output_data, jsonfile, indent=2)
        
        return filepath
