from application.metrics.base_metric import BaseMetric


class CAF(BaseMetric):

    def __init__(self, documentation_data: dict):
        super().__init__(
            metric_id="M_CAF",
            name="CAF",
            dimension="formal"
        )

        self.documentation_data = documentation_data

        self.weights = {
            "activities": 0.30,
            "rules": 0.20,
            "roles": 0.15,
            "artifacts": 0.20,
            "sequence": 0.10,
            "metrics": 0.05
        }

    def calculate(self, model=None, violations=None):

        # -----------------------------
        # Totales desde el JSON
        # -----------------------------

        total_activities = sum(len(p.activities) for p in model.practices)
        total_rules = len(model.practices)
        total_roles = len({r.id for p in model.practices for r in p.roles})
        total_artifacts = len({a.id for p in model.practices for a in p.artifacts})
        total_sequence = len(model.compatibility_relations)
        total_metrics = 1  # asumimos al menos el sistema métrico existe

        # -----------------------------
        # Documentados
        # -----------------------------

        documented_activities = sum(
            1
            for a in self.documentation_data.get(
                "activities", []
            )
            if a.get("documented", False)
        )

        documented_rules = sum(
            1
            for r in self.documentation_data.get(
                "rules", []
            )
            if r.get("documented", False)
        )

        documented_roles = sum(
            1
            for r in self.documentation_data.get(
                "roles", []
            )
            if r.get("documented", False)
        )

        documented_artifacts = sum(
            1
            for a in self.documentation_data.get(
                "artifacts", []
            )
            if a.get("documented", False)
        )

        documented_sequence = sum(
            1
            for s in self.documentation_data.get(
                "sequence", []
            )
            if s.get("documented", False)
        )

        documented_metrics = sum(
            1
            for m in self.documentation_data.get(
                "metrics", []
            )
            if m.get("documented", False)
        )

        # -----------------------------
        # Normalización
        # -----------------------------

        scores = {}

        scores["activities"] = (
            documented_activities / total_activities
            if total_activities > 0 else 1
        )

        scores["rules"] = (
            documented_rules / total_rules
            if total_rules > 0 else 1
        )

        scores["roles"] = (
            documented_roles / total_roles
            if total_roles > 0 else 1
        )

        scores["artifacts"] = (
            documented_artifacts / total_artifacts
            if total_artifacts > 0 else 1
        )

        scores["sequence"] = (
            documented_sequence / total_sequence
            if total_sequence > 0 else 1
        )

        scores["metrics"] = (
            documented_metrics / total_metrics
            if total_metrics > 0 else 1
        )

        # -----------------------------
        # Ponderación
        # -----------------------------

        caf = sum(
            scores[k] * self.weights[k]
            for k in self.weights
        )

        return caf * 100

    def interpret(self, value: float) -> str:

        if value > 80:
            return (
                "Alta cobertura formal, "
                "proceso maduro y replicable"
            )

        elif value >= 60:
            return (
                "Cobertura moderada, "
                "existen áreas de mejora"
            )

        else:
            return (
                "Baja formalización, "
                "alto riesgo de dependencia informal"
            )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )