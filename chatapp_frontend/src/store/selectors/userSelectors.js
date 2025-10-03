const userSelector = (state) => {
    return state.users
}

export const GetUsers = (state) => {
    return userSelector(state)?.users_list
}