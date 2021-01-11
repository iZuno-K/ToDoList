import camelcaseKeys from 'camelcase-keys'
import KanbanClient from "../../../utils/kanbanClient";

const state = {
    boardData: {
        pipLineList: [],
    },
    focusedCard: {}, // opened card
};

const getters = {
    getSocket(state, getters, rootState) {
        return rootState.socket;
    },
    getFilteredPipeLineList(state) {
        return state.boardData.pipeLineList;
    },
    getBoardId(state) {
        return state.boardData.boardId;
    },
};

const actions = {
    updateCardOrder({commit, getters}, {pipeLineId, cardList}) {
        console.log(pipeLineId, cardList);
        const socket = getters.getSocket;
        socket.sendObj({
            type: 'update_card_order',
            pipeLineId,
            cardIdList: cardList.map(x => x.cardId),
        });
        commit('updateCardOrder', {pipeLineId, cardList});
    },
    async addCard({commit, getters}, {pipeLineId, cardTitle}) {
        console.log(pipeLineId, cardTitle);
        const socket = getters.getSocket;
        await KanbanClient.addCard({
            pipeLineId,
            cardTitle,
        });
        socket.sendObj({
            type: 'broadcast_board_data',
            pipeLineId,
            cardTitle,
        });
        // dispatch('broadcastBoardData');
    },
    async fetchFocusedCard({commit}, {boardId, cardId}) {
        const cardData = await KanbanClient.getCardData({boardId, cardId});
        commit('setFocusedCard', cardData);
    },
    async updateCardContent({commit}, {boardId, cardId, content, expectedEffort, realEffort, completeTime, taskState,}) {
        const cardData = await KanbanClient.updateCardData({
            boardId,
            cardId,
            content,
            expectedEffort,
            realEffort,
            completeTime,
            taskState,
        });
        console.log(cardData);
        commit('setFocusedCard', cardData);
    },
    async updateCardTitle({commit, getters}, {boardId, cardId, title}) {
        const cardData = await KanbanClient.updateCardData({
            boardId,
            cardId,
            title,
        });
        commit('setFocusedCard', cardData);
        const socket = getters.getSocket;
        socket.sendObj({type: 'broadcast_board_data',});
        // dispatch('broadcast_board_data');
    },
    async deleteCard({getters}, {boardId, cardId}) {
        await KanbanClient.deleteCard({
            boardId,
            cardId,
        });
        // dispatch('broadcast_board_data');
        const socket = getters.getSocket;
        socket.sendObj({type: 'broadcast_board_data',});

    },
    addPipeLine({ getters }, { boardId, pipeLineName }) {
        console.log(boardId, pipeLineName);
        const socket = getters.getSocket;
        socket.sendObj({
            type: 'add_pipe_line',
            boardId,
            pipeLineName,
        });
    },
    renamePipeLine({ getters }, { pipeLineId, pipeLineName }) {
        const socket = getters.getSocket;
        socket.sendObj({
            type: 'rename_pipe_line',
            pipeLineId,
            pipeLineName,
        });
    },
    deletePipeLine({ getters }, { boardId, pipeLineId }) {
        console.log(boardId, pipeLineId);
        const socket = getters.getSocket;
        socket.sendObj({
            type: 'delete_pipe_line',
            boardId,
            pipeLineId,
        });
    },
    async updateBoardContent({commit}, {boardId, startDate, endDate,}) {
        const boardData = await KanbanClient.updateBoard({
            boardId,
            startDate,
            endDate,
        });
        // commit('setFocusedCard', cardData);
    },
    async updateBoardTitle({commit, getters}, {boardId, name}) {
        console.log("updateBoardTitle", boardId, name);
        const boardData = await KanbanClient.updateBoard({
            boardId,
            name,
        });
        // commit('setFocusedCard', cardData);
        const socket = getters.getSocket;
        socket.sendObj({type: 'broadcast_board_data',});
        // dispatch('broadcast_board_data');
    },
};

const mutations = {
    updateCardOrder(state, {pipeLineId, cardList}) { // update order of a certain pipeline
        const targetPipeLine = state.boardData.pipeLineList.find(pipeLine => pipeLine.pipeLineId === pipeLineId);
        targetPipeLine.cardList = cardList;
    },
    setBoardData(state, {boardData}) {
        console.log("boardData", boardData);
        state.boardData = camelcaseKeys(boardData, {deep: true});
    },
    setFocusedCard(state, cardData) {
        state.focusedCard = cardData;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
