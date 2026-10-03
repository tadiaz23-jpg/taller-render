"""
Servicio de Feature Toggles utilizando ConfigCat SDK con modo fallback/local para CI/CD y Pruebas.
"""
import os
import configcatclient
from configcatclient.user import User

class FeatureToggleService:
    def __init__(self, sdk_key: str = None):
        self.sdk_key = sdk_key or os.getenv("CONFIGCAT_SDK_KEY", "")
        self._overrides = {}
        
        if self.sdk_key:
            # Inicializar cliente real de ConfigCat
            self.client = configcatclient.get(self.sdk_key)
        else:
            # Modo fallback/local para entornos sin API Key activa
            self.client = None
            # Valores por defecto para desarrollo local
            self._overrides = {
                "multiplicacion_enabled": True,
                "division_enabled": False  # En desarrollo, la división puede estar en rollout progresivo
            }

    def is_feature_enabled(self, key: str, default_value: bool = False, user_id: str = "default_user") -> bool:
        """
        Verifica si un Feature Toggle está habilitado.
        Soporta targeting de usuarios y overrides locales para testing.
        """
        if key in self._overrides:
            return self._overrides[key]

        if self.client:
            user = User(user_id) if user_id else None
            return self.client.get_value(key, default_value, user)

        return default_value

    def set_override(self, key: str, value: bool):
        """Permite forzar el estado de un toggle durante las pruebas unitarias."""
        self._overrides[key] = value

    def clear_overrides(self):
        self._overrides.clear()

    def close(self):
        if self.client:
            self.client.close()

# Instancia global reutilizable
feature_toggle_service = FeatureToggleService()
