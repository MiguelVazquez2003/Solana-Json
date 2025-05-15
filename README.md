
## Descripción

Este script permite:
- Obtener información detallada de un slot específico de la red Solana
- Verificar si una cuenta específica participó en las transacciones de ese slot
- Guardar toda la información en formato JSON para análisis posterior

## Requisitos

- Bibliotecas requeridas:
  - requests
  - solathon


## Uso

```bash
python tarea.py <número_de_slot> [dirección_de_cuenta]
```

### Parámetros:
- `número_de_slot`: El número del slot de Solana que desea consultar
- `dirección_de_cuenta`: Dirección de cuenta para verificar su participación

### Ejemplo:

```bash
python tarea.py 340223016 AKzmVHRNPZx8SfC13RYEfBLMiNDM9p4SpZ1BxaLbsbuf
```

Salida:
```
Obteniendo información del slot 340223016...
Verificando participación de la cuenta: AKzmVHRNPZx8SfC13RYEfBLMiNDM9p4SpZ1BxaLbsbuf
Enviando solicitud RPC para obtener información del bloque 340223016
Información del bloque recibida
Información guardada en: slot_340223016.json
La cuenta AKzmVHRNPZx8SfC13RYEfBLMiNDM9p4SpZ1BxaLbsbuf SI participó en el slot 340223016
```

## Archivos generados

El script genera un archivo JSON por cada consulta con el nombre `slot_<número>.json` que contiene toda la información del slot, incluyendo:
- Datos del bloque
- Transacciones incluidas
- Resultado de la verificación de la cuenta (si se proporcionó)

