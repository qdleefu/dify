from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage
from typing import Any, Dict, List, Union
import requests


class OdooVersionTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
                tool_paramters: Dict[str, Any],
                ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        credentials = self.runtime.credentials
        odoo_url = credentials['odoo_url']
        odoo_db = credentials['odoo_db']
        odoo_username = credentials['odoo_username']
        odoo_password = credentials['odoo_password']

        try:
            # Authenticate with Odoo
            auth_url = f"{odoo_url}/web/session/authenticate"
            auth_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "db": odoo_db,
                    "login": odoo_username,
                    "password": odoo_password,
                },
                "id": 1,
            }
            auth_response = requests.post(auth_url, json=auth_payload).json()
            if auth_response.get("error"):
                return self.create_text_message(text="Authentication failed.")

            # Fetch version information
            version_url = f"{odoo_url}/web/webclient/version_info"
            version_response = requests.get(version_url).json()
            version_info = version_response.get("server_version", "Unknown version")

            return self.create_text_message(text=f"Odoo version: {version_info}")
        except Exception as e:
            return self.create_text_message(text=f"Error: {str(e)}")
