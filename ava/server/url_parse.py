class UrlParse():
    """
    Minimalist class that help to parse URL and get their parameters.
    """

    def __init__(self, url):
        """
        Initializer

            @param url: the url to handle
            @type url: string
        """
        self._url_split = [x for x in url.split('/') if x]
        self._url = url

    def __str__(self):
        """
        Pretty printing
        """
        return self._url

    def __repr__(self):
        """
        Pretty printing in interpretor
        """
        return self._url

    def __hash__(self):
        """
        Create a unique hash for each URL
        """
        return hash(self._url)

    def __eq__(self, other_str):
        """
        Compare an URLParse object and a route to know if they match

            @param other_str: route to check
            @type other_str: string
            @return: if the URLParse object match the route
            @rtype: bool
        """
        other_url_split = [x for x in other_str.split('/') if x]
        if len(self._url_split) != len(other_url_split):
            return False
        for squerry, oquerry in zip(self._url_split, other_url_split):
            if squerry[0] != ':' and squerry != oquerry:
                return False
        return True

    def get_url_var(self, other_str):
        """
        Get the parameters from the URL (using the REST notation system)

        @param other_str: the URL you want to extract parameters
        @type other_str: string
        @return: dictionnary with name and value of the parameters
        @rtype: Dictionnary
        """
        other_split = [x for x in other_str.split('/') if x]
        url_vars = {}
        for squerry, oquerry in zip(self._url_split, other_split):
            if squerry[0] == ':':
                url_vars[squerry[1:]] = oquerry

        return url_vars
