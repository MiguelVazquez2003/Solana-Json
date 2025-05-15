import json
import sys
import requests
from solathon.publickey import PublicKey

def get_slot_info(slot_number, account_address=None):
    """
    Obtiene información de un slot específico y verifica si una cuenta participó en él.
    
    Args:
        slot_number (int): Número del slot a consultar
        account_address (str): Dirección de la cuenta a verificar (opcional)
    
    Returns:
        dict: Información del slot y resultado de la verificación
    """
    # URL del endpoint de Solana para llamadas RPC
    rpc_url = "https://api.mainnet-beta.solana.com"
    
    try:
        # Preparar la solicitud JSON-RPC para obtener información del bloque
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [
                slot_number,
                {
                    "encoding": "json",
                    "maxSupportedTransactionVersion": 0
                }
            ]
        }
        
        print(f"Enviando solicitud RPC para obtener información del bloque {slot_number}")
        response = requests.post(rpc_url, headers=headers, json=payload)
        response_data = response.json()
        
        # Verificar si hay errores en la respuesta
        if "error" in response_data:
            error_msg = response_data["error"]["message"]
            raise Exception(f"Error en la solicitud RPC: {error_msg}")
        
        # Obtener información del bloque
        block_info = response_data.get("result", {})
        print(f"Información del bloque recibida")
        
        # Preparar el resultado
        result = {
            "slot": slot_number,
            "block_info": block_info,
            "account_participation": False,
            "account_address": account_address
        }
        
        # Verificar si la cuenta participó en este slot (si se proporcionó una dirección)
        if account_address:
            account_pubkey = PublicKey(account_address)
            print(f"Verificando participación de la cuenta: {account_pubkey}")
            
            # Verificar transacciones para ver si la cuenta participó
            participation = False
            
            if block_info and "transactions" in block_info:
                for tx in block_info["transactions"]:
                    # Verificar si la cuenta es remitente o receptor en alguna transacción
                    if "transaction" in tx and "message" in tx["transaction"]:
                        message = tx["transaction"]["message"]
                        
                        # Buscar en las cuentas involucradas
                        if "accountKeys" in message:
                            for account_key in message["accountKeys"]:
                                if account_key == account_address:
                                    participation = True
                                    break
                    
                    if participation:
                        break
            
            result["account_participation"] = participation
        
        return result
    
    except Exception as e:
        return {
            "error": str(e),
            "slot": slot_number,
            "account_address": account_address
        }

def save_slot_info_to_json(slot_info, output_filename=None):
    """
    Guarda la información del slot en un archivo JSON
    
    Args:
        slot_info (dict): Información del slot
        output_filename (str): Nombre del archivo de salida (opcional)
    
    Returns:
        str: Ruta del archivo guardado
    """
    if not output_filename:
        slot_number = slot_info.get("slot", "unknown")
        output_filename = f"slot_{slot_number}.json"
    
    with open(output_filename, 'w') as f:
        json.dump(slot_info, f, indent=2)
    
    return output_filename

def main():
    """Función principal que procesa los argumentos y ejecuta el programa"""
    if len(sys.argv) < 2:
        print("Uso: python tarea.py <número_de_slot> [dirección_de_cuenta]")
        print("Ejemplo: python tarea.py 123456789 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin")
        return
    
    try:
        slot_number = int(sys.argv[1])
        account_address = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"Obteniendo información del slot {slot_number}...")
        if account_address:
            print(f"Verificando participación de la cuenta: {account_address}")
        
        slot_info = get_slot_info(slot_number, account_address)
        
        if "error" in slot_info:
            print(f"Error: {slot_info['error']}")
            return
        
        output_file = save_slot_info_to_json(slot_info)
        print(f"Información guardada en: {output_file}")
        
        if account_address:
            if slot_info["account_participation"]:
                print(f"✓ La cuenta {account_address} SÍ participó en el slot {slot_number}")
            else:
                print(f"✗ La cuenta {account_address} NO participó en el slot {slot_number}")
    
    except ValueError:
        print("Error: El número de slot debe ser un entero")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()