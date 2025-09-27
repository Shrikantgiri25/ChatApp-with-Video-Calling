const chatSelector = (state) => {
    return state.chats
}

export const GetUserChatHistory = (state) => {
    return chatSelector(state)?.chatHistory
}