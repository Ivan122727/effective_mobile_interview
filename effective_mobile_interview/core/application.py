from effective_mobile_interview.create_application import create_app

def start_app():
    """Функция для запуска проекта"""
    app = create_app()
    path = "/index_page" # Главная страница
    method = "GET"
    body = None
    request_res = app.process_interface_request(path="/index_page", method="GET")
    while request_res.status == 200:
        if "path" in request_res.result:
            path = request_res.result["path"]
            method = request_res.result["method"]
        if "api_url" in request_res.result:
            api_request_res = app.process_api_request(
                path=request_res.result["api_url"], 
                method=request_res.result["api_method"], 
                body=request_res.result.get("body", None)
            )
            body = api_request_res.result
        else:
            body = None
        request_res = app.process_interface_request(
            path=path, 
            method=method, 
            body=body
        )