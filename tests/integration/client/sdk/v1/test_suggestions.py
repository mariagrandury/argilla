#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
from argilla.client.client import Argilla
from argilla.client.sdk.v1.suggestions.api import delete_suggestion
from argilla.server.models import UserRole

from tests.factories import (
    DatasetFactory,
    RecordFactory,
    SuggestionFactory,
    UserFactory,
)


@pytest.mark.asyncio
class TestSuggestionsSDK:
    @pytest.mark.parametrize("role", [UserRole.owner, UserRole.admin])
    async def test_delete_suggestions(self, role: UserRole) -> None:
        dataset = await DatasetFactory.create()
        record = await RecordFactory.create(dataset=dataset)
        suggestion = await SuggestionFactory.create(record=record)
        user = await UserFactory.create(role=role, workspaces=[dataset.workspace])

        api = Argilla(api_key=user.api_key, workspace=dataset.workspace.name)

        response = delete_suggestion(client=api.client.httpx, id=suggestion.id)
        assert response.status_code == 200
        assert response.parsed.id == suggestion.id
