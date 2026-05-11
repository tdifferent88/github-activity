import sys

import requests


def buscar_atividade(usuario):
    """
    Busca atividades públicas recentes de um usuário no GitHub.
    """

    url = f"https://api.github.com/users/{usuario}/events"

    try:
        resposta = requests.get(url, timeout=10)

    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão: {erro}")
        return None

    if resposta.status_code == 404:
        print("Usuário não encontrado.")
        return None

    if resposta.status_code != 200:
        print(f"Erro ao buscar dados. Código: {resposta.status_code}")
        return None

    return resposta.json()


def formatar_evento(evento):
    """
    Formata os eventos retornados pela API do GitHub.
    """

    tipo = evento.get("type", "Evento desconhecido")

    repositorio = evento.get(
        "repo",
        {}
    ).get(
        "name",
        "repositório desconhecido"
    )

    payload = evento.get("payload", {})

    # Evento de push
    if tipo == "PushEvent":

        commits = payload.get("commits", [])

        quantidade = len(commits)

        if quantidade == 0:
            return f"- Fez push em {repositorio}"

        return f"- Fez {quantidade} commit(s) em {repositorio}"

    # Evento de issue
    elif tipo == "IssuesEvent":

        acao = payload.get("action", "alterou")

        return f"- {acao.capitalize()} uma issue em {repositorio}"

    # Evento de star
    elif tipo == "WatchEvent":

        return f"- Deu star em {repositorio}"

    # Evento de fork
    elif tipo == "ForkEvent":

        return f"- Fez fork de {repositorio}"

    # Evento de criação
    elif tipo == "CreateEvent":

        ref_type = payload.get("ref_type", "algo")

        return f"- Criou {ref_type} em {repositorio}"

    # Evento de pull request
    elif tipo == "PullRequestEvent":

        acao = payload.get("action", "alterou")

        return f"- {acao.capitalize()} um pull request em {repositorio}"

    # Qualquer outro evento
    else:

        return f"- {tipo} em {repositorio}"


def exibir_atividade(usuario):
    """
    Exibe as atividades recentes do usuário.
    """

    eventos = buscar_atividade(usuario)

    if not eventos:
        print("Nenhuma atividade recente encontrada.")
        return

    print(f"\nAtividade recente de {usuario}:\n")

    # Limita aos 10 eventos mais recentes
    for evento in eventos[:10]:

        print(formatar_evento(evento))


def main():
    """
    Função principal do programa.
    """

    # Verifica se o usuário informou o username
    if len(sys.argv) < 2:

        print("Uso correto:")
        print("python github_activity.py <usuario>")

        return

    usuario = sys.argv[1]

    exibir_atividade(usuario)


# Executa o programa
if __name__ == "__main__":

    main()
