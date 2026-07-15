from collections import defaultdict
from unittest import result


class CertaintyFactorService:

    @staticmethod
    def calculate_cf(cf_user: float, cf_expert: float) -> float:
        """
        CF(H,E) = CF User × CF Pakar
        """
        return cf_user * cf_expert

    @staticmethod
    def combine_cf(cf_values: list[float]) -> float:
        """
        Menggabungkan beberapa nilai CF.

        Rumus:
        CFcombine = CF1 + CF2 × (1 - CF1)
        """

        if not cf_values:
            return 0

        result = cf_values[0]

        for cf in cf_values[1:]:
            result = result + (cf * (1 - result))

        return round(result, 4)

    @staticmethod
    def to_percentage(cf: float) -> float:
        """
        Mengubah nilai CF menjadi persentase.
        """
        return round(cf * 100, 2)

    @staticmethod
    def get_urgency(percentage: float) -> str:
        """
        Menentukan tingkat urgensi berdasarkan persentase diagnosis.
        """

        if percentage >= 90:
            return "darurat"

        elif percentage >= 70:
            return "tinggi"

        elif percentage >= 40:
            return "sedang"

        return "rendah"

    @staticmethod
    def calculate(user_symptoms, rules, diseases):
        """
        Menghitung seluruh penyakit berdasarkan gejala
        yang dipilih oleh user.
        """

        disease_cf = defaultdict(list)

        # Mapping gejala user
        user_cf = {
            item["symptom_id"]: item["cf_user"]
            for item in user_symptoms
        }

        # Hitung CF setiap rule
        for rule in rules:

            symptom_id = rule["symptom_id"]

            if symptom_id not in user_cf:
                continue

            cf = CertaintyFactorService.calculate_cf(
                user_cf[symptom_id],
                float(rule["cf_expert"])
            )

            disease_cf[rule["disease_id"]].append(cf)

        results = []

        # Hitung hasil tiap penyakit
        for disease in diseases:

            disease_id = disease["id"]

            values = disease_cf.get(disease_id, [])

            if not values:
                continue

            final_cf = CertaintyFactorService.combine_cf(values)

            # Salin seluruh data penyakit
            result = disease.copy()

            # Tambahkan hasil perhitungan
            result["cf_value"] = final_cf
            result["percentage"] = CertaintyFactorService.to_percentage(final_cf)
            result["urgency_level"] = CertaintyFactorService.get_urgency(
                result["percentage"]
            )

            results.append(result)

        # Urutkan berdasarkan persentase terbesar
        results.sort(
            key=lambda x: x["percentage"],
            reverse=True
        )

        # Tambahkan ranking
        for i, item in enumerate(results, start=1):
            item["rank"] = i

        return results