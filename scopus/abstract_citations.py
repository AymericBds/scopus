from collections import namedtuple
from datetime import datetime
from json import loads
from os.path import join

from scopus import config
from scopus.utils import get_content


class CitationOverview(object):
    @property
    def authors(self):
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is (name surname initials id url).
        All entries are strings.
        """
        out = []
        order = 'name surname initials id url'
        auth = namedtuple('Author', order)
        for author in self._citeInfoMatrix.get('author'):
            author = {k.split(":", 1)[-1]: v for k, v in author.items()}
            new = auth(name=author.get('index-name'),
                       surname=author.get('surname'),
                       initials=author.get('initials'),
                       id=author.get('authid'),
                       url=author.get('author-url'))
            out.append(new)
        return out

    @property
    def cc(self):
        """List of tuples of yearly number of citations
        for specified years."""
        _years = range(self._start, self._end+1)
        try:
            return list(zip(_years, [d.get('$') for d in self._citeInfoMatrix['cc']]))
        except AttributeError:  # No citations
            return list(zip(_years, [0]*len(_years)))

    @property
    def citationType_long(self):
        """Type (long version) of the abstract (e.g. article, review)."""
        return self._citeInfoMatrix.get('citationType', {}).get('$')

    @property
    def citationType_short(self):
        """Type (short version) of the abstract (e.g. ar, re)."""
        return self._citeInfoMatrix.get('citationType', {}).get('@code')

    @property
    def doi(self):
        """Document Object Identifier (DOI) of the abstract."""
        return self._identifierlegend.get('doi')

    @property
    def endingPage(self):
        """Ending page."""
        return self._citeInfoMatrix.get('endingPage')

    @property
    def h_index(self):
        """h-index of ciations of the abstract (according to Scopus)."""
        return self._data['h-index']

    @property
    def issn(self):
        """ISSN of the publisher.
        Note: If E-ISSN is known to Scopus, this returns both
        ISSN and E-ISSN in random order separated by blank space.
        """
        return self._citeInfoMatrix.get('issn')

    @property
    def issueIdentifier(self):
        """Issue number for abstract."""
        return self._citeInfoMatrix.get('issueIdentifier')

    @property
    def lcc(self):
        """Number of citations the abstract received
        after the specified end year.
        """
        return self._citeInfoMatrix.get('lcc')

    @property
    def pcc(self):
        """Number of citations the abstract received
        before the specified start year.
        """
        return self._citeInfoMatrix.get('pcc')

    @property
    def pii(self):
        """The Publication Item Identifier (PII) of the abstract."""
        return self._identifierlegend.get('pii')

    @property
    def publicationName(self):
        """Name of source the abstract is published in (e.g. the Journal)."""
        return self._citeInfoMatrix.get('publicationName')

    @property
    def scopus_id(self):
        """The Scopus ID of the abstract.  It is the second part of an EID.
        The Scopus ID might differ from the one provided.
        """
        return self._identifierlegend.get('scopus_id')

    @property
    def startingPage(self):
        """Starting page."""
        return self._citeInfoMatrix.get('startingPage')

    @property
    def rangeCount(self):
        """Number of citations for specified years."""
        return self._citeInfoMatrix.get('rangeCount')

    @property
    def rowTotal(self):
        """Number of citations (specified and omitted years)."""
        return self._citeInfoMatrix.get('rowTotal')

    @property
    def title(self):
        """Abstract title."""
        return self._citeInfoMatrix.get('title')

    @property
    def url(self):
        """URL to Citation Overview API view of the abstract."""
        return self._citeInfoMatrix.get('url')

    @property
    def volume(self):
        """Volume for the abstract."""
        return self._citeInfoMatrix.get('volume')

    def __init__(self, eid, start, end=datetime.now().year, refresh=False):
        """Class to represent the results from a Scopus Citation Overview.
        See https://api.elsevier.com/documentation/guides/AbstractCitationViews.htm.

        Parameters
        ----------
        eid : str
            The EID of the abstract.

        start : str or int
            The first year for which the citation count should be loaded

        end : str or int (optional, default=datetime.now().year)
            The last year for which the citation count should be loaded.
            Default is the current year.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Notes
        -----
        The files are cached in ~/.scopus/citation_overview/{eid}.
        Your API Key needs to be approved by Elsevier to access this view.
        """
        # Get file content
        scopus_id = eid.split('0-')[-1]
        qfile = join(config.get('Directories', 'CitationOverview'), eid)
        url = "https://api.elsevier.com/content/abstract/citations/{}".format(scopus_id)
        params = {'scopus_id': scopus_id, 'date': '{}-{}'.format(start, end)}
        res = get_content(qfile, url=url, refresh=refresh, params=params,
                          accept='json')
        self._data = loads(res.decode('utf-8'))['abstract-citations-response']

        self._start = int(start)
        self._end = int(end)

        # citeInfoMatrix
        m = self._data['citeInfoMatrix']['citeInfoMatrixXML']['citationMatrix']['citeInfo'][0]
        self._citeInfoMatrix = {k.split(":", 1)[-1]: v for k, v in m.items()}
        # identifier-legend
        l = self._data['identifier-legend']['identifier'][0]
        self._identifierlegend = {k.split(":", 1)[-1]: v for k, v in l.items()}
        # citeColumnTotalXML
        self._citeColumnTotalXML = self._data['citeColumnTotalXML']  # not used
