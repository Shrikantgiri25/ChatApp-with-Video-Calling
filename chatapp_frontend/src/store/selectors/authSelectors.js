const authSelector = (state) => {
    return state.auth
}

export const UserProfileDetails = (state) => {
    return authSelector(state)?.user
}