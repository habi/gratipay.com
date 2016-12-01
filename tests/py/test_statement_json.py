from __future__ import print_function, unicode_literals

import json

from gratipay.testing import Harness


class Tests(Harness):

    def change_statement(self, lang, statement, auth_as='alice',
            expecting_error=False):
        self.make_participant('alice', claimed_time='now')

        method = self.client.POST if not expecting_error else self.client.PxST
        response = method( "/~alice/statement.json"
                         , {'lang': lang, 'content': statement}
                         , auth_as=auth_as
                          )
        return response

    def test_participant_can_change_their_statement(self):
        response = self.change_statement('en', 'Lorem ipsum')
        actual = json.loads(response.body)['html']
        assert actual == '<p>Lorem ipsum</p>\n'

    def test_anonymous_gets_401(self):
        response = self.change_statement( 'en'
                                        , 'Some statement'
                                        , auth_as=None
                                        , expecting_error=True
                                         )
        assert response.code == 401, response.code

    def test_participant_cannot_change_their_statement_if_too_big(self):
        too_big_statement = 'A' * ((256 * 1024) + 1)
        response = self.change_statement('en', too_big_statement, expecting_error=True)
        assert response.code == 400
        assert response.body == 'Statement too big!'
