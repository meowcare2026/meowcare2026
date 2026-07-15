from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class PdfService:

    @staticmethod
    def generate(data):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Laporan Diagnosis Kucing</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                f"Pemilik : {data['owner_name']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Nama Kucing : {data['cat_name']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Umur : {data['cat_age']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Jenis Kelamin : {data['cat_gender']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Penyakit : {data['diseases']['name']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Persentase : {data['highest_percentage']}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Tingkat Urgensi : {data['urgency_level']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Rekomendasi : {data['recommendation']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                data["disclaimer"],
                styles["Italic"]
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer