from urllib.parse import urlparse


def get_domain(url):
    """
    get domain name of given url
    :param url: str -> https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46
    :return: str -> medium.com
    """
    if url:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    else:
        return ''
