import axios from 'axios';
import {loadProgressBar} from 'axios-progress-bar';
import camelcaseKeys from 'camelcase-keys';
import board from "../src/store/pages/board";


const _handleSuccess = response => {
    console.log(response.data);
    // すべてのJSONのキーをスネークケースからキャメルケースに変換する
    response.data = camelcaseKeys(response.data, {deep: true});
    return response;
};

class Client {
    constructor() {
        this.service = axios.create();
        this.service.interceptors.response.use(_handleSuccess);
        loadProgressBar({showSpinner: false}, this.service);
    }

    _get(path, payload) {
        return this.service.get(path, payload);
    }

    _patch(path, payload) {
        return this.service.patch(path, payload);
    }

    _post(path, payload, config = {}) {
        return this.service.post(path, payload, config);
    }

    _put(path, payload) {
        return this.service.put(path, payload);
    }

    _delete(path) {
        return this.service.delete(path);
    }
}

class KanbanClient extends Client {
    constructor() {
        super();
        this.baseUrl = '/api';
    }

    async getAccountInfo() {
        const response = await this._get(`${this.baseUrl}/accounts/`);
        return response.data.accountInfo;
    }

    async getBoardList() {
        const response = await this._get(`${this.baseUrl}/boards/`);
        return response.data.boardList;
    }

    async addBoard({boardName, startDate, endDate}) {
        await this._post(`${this.baseUrl}/boards/`, {
            boardName, startDate, endDate
        });
    }

    async addCard({cardTitle, pipeLineId}) {
        console.log(cardTitle);
        console.log(pipeLineId);
        await this._post(`${this.baseUrl}/cards/`, {
            cardTitle,
            pipeLineId,
        });
    }

    async getCardData({boardId, cardId}) {
        const response = await this._get(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`);
        console.log(response.data.cardData);
        return response.data.cardData;
    }

    async updateCardData({boardId, cardId, content, title, expectedEffort, realEffort, completeTime, taskState}) {
        const response = await this._patch(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`, {
            content, title, expectedEffort, realEffort, completeTime, taskState,
        });
        console.log(response.data.CardData);
        return response.data.cardData;
    }

    async deleteCard({boardId, cardId}) {
        await this._delete(`${this.baseUrl}/boards/${boardId}/cards/${cardId}/`);
    }

    async updateBoard({boardId, name, startDate, endDate}) {
        const response = await this._patch(`${this.baseUrl}/boards/${boardId}/boardInfo`, {
            name, startDate, endDate,
        });
        console.log(response.data.BoardData);
        return response.data.BoardData;
    }

}


export default new KanbanClient();