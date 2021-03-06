#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AuthorRetrieval` module."""

from collections import Counter
from nose.tools import assert_equal, assert_true

import scopus


au = scopus.AuthorRetrieval("7004212771", refresh=True)


def test_affiliation_current():
    assert_equal(au.affiliation_current, '110785688')


def test_affiliation_history():
    affs = au.affiliation_history
    assert_true(len(affs) >= 5)
    assert_true(isinstance(affs[0], unicode))


def test_citation_count():
    assert_true(au.citation_count >= '7584')


def test_cited_by_count():
    assert_true(au.cited_by_count >= '6066')


def test_coauthor_count():
    assert_true(au.coauthor_count >= '164')


def test_classificationgroup():
    groups = au.classificationgroup
    assert_true(isinstance(groups, list))
    assert_true(len(groups) > 0)
    assert_true(('1906', '1') in groups)  # frequency might differ


def test_coauthor_link():
    expected = 'http://api.elsevier.com/content/search/author?co-author=7004212771'
    assert_equal(au.coauthor_link, expected)


def test_date_created():
    assert_equal(au.date_created, (2005, 12, 3))


def test_document_count():
    assert_true(au.document_count >= '99')


def test_eid():
    assert_equal(au.eid, '9-s2.0-7004212771')


def test_given_name():
    assert_equal(au.given_name, 'John R.')


def test_h_index():
    assert_true(au.h_index >= '27')


def test_identifier():
    assert_equal(au.identifier, "7004212771")


def test_indexed_name():
    assert_equal(au.indexed_name, 'Kitchin J.')


def test_initials():
    assert_equal(au.initials, 'J.R.')


def test_journal_history():
    hist = au.journal_history
    assert_true(isinstance(hist, list))
    assert_true(len(hist) > 0)
    expected = ('ACS Catalysis', 'ACS Catal.', 'j', '21555435')
    assert_true(expected in hist)


def test_orcid():
    assert_equal(au.orcid, '0000-0003-2625-9232')


def test_name_variants():
    names = au.name_variants
    assert_true(isinstance(names, list))
    assert_true(len(names) > 0)
    expected = "<class 'scopus.author_retrieval.Variant'>"
    assert_equal(str(type(names[0])), expected)


def test_surname():
    assert_equal(au.surname, 'Kitchin')


def test_scopus_author_link():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(au.scopus_author_link, expected)


def test_self_link():
    expected = 'https://www.scopus.com/authid/detail.uri?partnerID=HzOxMe3b&'\
               'authorId=7004212771&origin=inward'
    assert_equal(au.self_link, expected)


def test_search_link():
    expected = 'http://api.elsevier.com/content/search/scopus?query='\
               'au-id%287004212771%29'
    assert_equal(au.search_link, expected)


def test_publication_range():
    assert_true(au.publication_range[0] <= '1995')
    assert_true(au.publication_range[1] >= '2018')


def test_subject_areas():
    areas = au.subject_areas
    assert_true(isinstance(areas, list))
    assert_true(len(areas) > 0)
    expected = "<class 'scopus.author_retrieval.Subjectarea'>"
    assert_equal(str(type(areas[0])), expected)


def test_url():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(au.url, expected)
