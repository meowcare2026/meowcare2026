from collections import defaultdict


class CertaintyFactorService:
    """
    Implementasi metode Certainty Factor.

    Tahapan:
    1. CF(H,E) = CF User × CF Pakar
    2. CF Combine
    3. Konversi ke persentase
    """

    # Nilai CF User yang diperbolehkan
    VALID_CF_VALUES = {0, 0.2, 0.4, 0.6, 0.8, 1}

    @staticmethod
    def calculate_cf(cf_user: float, cf_expert: float) -> float:
        """
        CF(H,E) = CF User × CF Pakar
        """

        if cf_user not in CertaintyFactorService.VALID_CF_VALUES:
            raise ValueError(
                f"Nilai CF User tidak valid: {cf_user}"
            )

        cf = cf_user * cf_expert

        # menjaga nilai tetap antara 0 - 1
        return max(0, min(round(cf, 4), 1))

    @staticmethod
    def combine_cf(cf_values: list[float]) -> float:
        """
        Menggabungkan beberapa CF menggunakan rumus:

        CFcombine = CF1 + CF2 × (1 − CF1)
        """

        if not cf_values:
            return 0

        # Urutkan dari terbesar
        cf_values = sorted(cf_values, reverse=True)

        combined = cf_values[0]

        for cf in cf_values[1:]:
            combined = combined + (cf * (1 - combined))

        return round(combined, 4)

    @staticmethod
    def to_percentage(cf: float) -> float:
        """
        Mengubah nilai CF menjadi persentase.
        """

        return round(cf * 100, 2)

    @staticmethod
    def get_urgency(percentage: float) -> str:
        """
        Tingkat keyakinan hasil diagnosis.
        (Tambahan untuk kebutuhan aplikasi)
        """

        if percentage >= 90:
            return "darurat"

        elif percentage >= 70:
            return "tinggi"

        elif percentage >= 40:
            return "sedang"

        return "rendah"

    @staticmethod
    def calculate(
        user_symptoms,
        rules,
        diseases,
    ):
        """
        Menghitung seluruh kemungkinan penyakit.
        """

        disease_cf = defaultdict(list)

        # Mapping gejala yang dipilih user
        user_cf = {
            item["symptom_id"]: item["cf_user"]
            for item in user_symptoms
        }

        # Hitung CF setiap rule
        for rule in rules:

            symptom_id = rule["symptom_id"]

            if symptom_id not in user_cf:
                continue

            cf_value = CertaintyFactorService.calculate_cf(
                user_cf[symptom_id],
                float(rule["cf_expert"])
            )

            disease_cf[rule["disease_id"]].append({
                "symptom_id": symptom_id,
                "cf_user": user_cf[symptom_id],
                "cf_expert": float(rule["cf_expert"]),
                "cf_result": cf_value,
            })

        results = []

        # Hitung setiap penyakit
        for disease in diseases:

            disease_id = disease["id"]

            calculations = disease_cf.get(disease_id, [])

            if not calculations:
                continue

            cf_values = [
                item["cf_result"]
                for item in calculations
            ]

            final_cf = CertaintyFactorService.combine_cf(
                cf_values
            )

            disease_result = disease.copy()

            disease_result["cf_value"] = final_cf
            disease_result["percentage"] = (
                CertaintyFactorService.to_percentage(
                    final_cf
                )
            )

            disease_result["urgency_level"] = (
                CertaintyFactorService.get_urgency(
                    disease_result["percentage"]
                )
            )

            # Tambahan informasi
            disease_result["matched_symptoms"] = len(
                calculations
            )

            disease_result["calculation_details"] = calculations

            results.append(disease_result)

        # Urutkan berdasarkan persentase terbesar
        results.sort(
            key=lambda x: x["percentage"],
            reverse=True,
        )

        # Ranking hasil
        for rank, disease in enumerate(
            results,
            start=1,
        ):
            disease["rank"] = rank

        return results