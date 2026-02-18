def get_download_link(server: str, client_id: str, secret_key: str, device_id: str) -> str:
    # 1. Получение токена
    token_url = "/v1.0/token?grant_type=1"
    token_resp = tuyarequest(server, token_url, client_id, secret_key)

    if not token_resp.get("success"):
        msg = token_resp.get("msg", "")
        if msg == "clientId is invalid":
            raise ClientIDError("Invalid Client ID")
        elif msg == "sign invalid":
            raise ClientSecretError("Invalid Client Secret")
        elif "cross-region access is not allowed" in msg:
            raise ServerError("Wrong server region. Cross-region access is not allowed.")
        else:
            raise RuntimeError(f"Token request failed: {token_resp}")

    access_token = token_resp.get("result", {}).get("access_token")
    if not access_token:
        raise RuntimeError("No access_token in response")

    # 2. Запрос ссылки на карту
    map_url = f"/v1.0/users/sweepers/file/{device_id}/realtime-map"
    map_resp = tuyarequest(server, map_url, client_id, secret_key, token=access_token)

    if not map_resp.get("success"):
        msg = map_resp.get("msg", "")
        if msg == "permission deny":
            raise DeviceIDError("Invalid Device ID")
        else:
            raise RuntimeError(f"Map request failed: {map_resp}")

    download_link = map_resp.get("result")
    if not download_link:
        raise NotSupportedError("Vacuum not supported: API returned no realtime maps")

    return download_link  # исправлено
