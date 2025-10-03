// UserListPane.jsx
import { List, Avatar, Spin } from "antd";
import "../ChatListPane/ChatListPane.scss";
import { useEffect, useState, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userService } from "../../../services/userService";
import LoadingScreen from "../../spinner/Spinner";
import { GetUsers } from "../../../store/selectors/userSelectors";

const UserListPane = () => {
  const dispatch = useDispatch();
  const allUsers = useSelector(GetUsers);

  const [isLoading, setIsLoading] = useState(!allUsers);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const observerRef = useRef(null);
  const loadMoreRef = useRef(null);

  // Initial load
  useEffect(() => {
    if (!allUsers) {
      userService.getUsers(setIsLoading, dispatch, 1, setHasMore);
    } else {
      setIsLoading(false);
    }
  }, [allUsers, dispatch]);

  // Load more users
  const loadMoreUsers = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;

    setIsLoadingMore(true);
    const nextPage = page + 1;
    await userService.getUsers(() => {}, dispatch, nextPage, setHasMore);
    setPage(nextPage);
    setIsLoadingMore(false);
  }, [page, dispatch, isLoadingMore, hasMore]);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const options = { root: null, rootMargin: "100px", threshold: 0.1 };
    observerRef.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasMore && !isLoadingMore) {
        loadMoreUsers();
      }
    }, options);

    const currentTarget = loadMoreRef.current;
    if (currentTarget && !isLoading) observerRef.current.observe(currentTarget);

    return () => {
      if (currentTarget && observerRef.current) {
        observerRef.current.unobserve(currentTarget);
      }
    };
  }, [hasMore, isLoadingMore, isLoading, loadMoreUsers]);

  return (
    <div className="chat-list-pane">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <h2 className="chatapp-title">Users</h2>
          <List
            itemLayout="horizontal"
            dataSource={allUsers}
            renderItem={(user) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <Avatar
                      src={
                        user.profile_picture
                          ? `${import.meta.env.VITE_API_BASE_URL}${user.profile_picture}`
                          : undefined
                      }
                    >
                      {user.email?.[0]?.toUpperCase()}
                    </Avatar>
                  }
                  title={user.email}
                  description={user.bio}
                />
              </List.Item>
            )}
          />

          {/* Loading more indicator */}
          {isLoadingMore && (
            <div style={{ textAlign: "center", padding: "20px" }}>
              <Spin size="large" />
            </div>
          )}

          {/* Intersection observer target */}
          {hasMore && !isLoadingMore && <div ref={loadMoreRef} style={{ height: "20px" }} />}

          {/* End of list */}
          {!hasMore && allUsers?.length > 0 && (
            <div style={{ textAlign: "center", padding: "20px", color: "#999" }}>
              No more users
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default UserListPane;