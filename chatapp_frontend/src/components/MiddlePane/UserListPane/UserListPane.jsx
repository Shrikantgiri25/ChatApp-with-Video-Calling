import { List, Avatar, Checkbox, Tooltip } from "antd";
import "../ChatListPane/ChatListPane.scss";
import { useEffect, useState, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userService } from "../../../services/userService";
import LoadingScreen from "../../spinner/Spinner";
import { GetUsers } from "../../../store/selectors/userSelectors";
import { REMOVE_USERS } from "../../../store/actiontypes/constants";
import { ArrowRightOutlined } from "@ant-design/icons";
import GroupCreationForm from "./GroupCreationForm";
import { groupService } from "../../../services/groupService";

const UserListPane = ({ search, isGroupCreation = false, showGroupForm, setShowGroupForm, setCreateGroup }) => {
  const dispatch = useDispatch();
  const allUsers = useSelector(GetUsers);

  const [isLoading, setIsLoading] = useState(!allUsers);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  const observerRef = useRef(null);
  const loadMoreRef = useRef(null);

  // Group Creation Checkbox Logic (Optimized using Set)
  const [checkedItems, setCheckedItems] = useState(new Set());
  
  const handleCheckboxChange = useCallback((userId) => {
    setCheckedItems((prev) => {
      const newSet = new Set(prev);
      newSet.has(userId) ? newSet.delete(userId) : newSet.add(userId);
      return newSet;
    });
  }, []);

  // Handle group creation submission
  const handleGroupCreation = async (groupData, setSubmitting) => {      
      // Reset state after successful creation
      await groupService.createGroup(groupData, setSubmitting)
      
      setShowGroupForm(false);
      setCreateGroup(false);
      setCheckedItems(new Set());
  };

  // Handle back button from group form
  const handleBackFromGroupForm = () => {
    setShowGroupForm(false);
  };

  // Initial load
  useEffect(() => {
    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    userService
      .getUsers(setIsLoading, dispatch, 1, setHasMore)
      .finally(() => setTimeout(() => setIsInitialLoad(false), 100));

    return () => dispatch({ type: REMOVE_USERS });
  }, [dispatch]);

  // Search effect
  useEffect(() => {
    dispatch({ type: REMOVE_USERS });
    if (search === null || search === undefined) return;

    setPage(1);
    setHasMore(true);
    setIsLoading(true);
    setIsInitialLoad(true);

    const timerID = setTimeout(() => {
      userService
        .getUsers(setIsLoading, dispatch, 1, setHasMore, search)
        .finally(() => setTimeout(() => setIsInitialLoad(false), 100));
    }, 800);

    return () => clearTimeout(timerID);
  }, [search, dispatch]);

  // Load more users (infinite scroll)
  const loadMoreUsers = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;
    setIsLoadingMore(true);
    const nextPage = page + 1;
    await userService.getUsers(() => {}, dispatch, nextPage, setHasMore, search);
    setPage(nextPage);
    setIsLoadingMore(false);
  }, [page, dispatch, isLoadingMore, hasMore, search]);

  // Intersection Observer
  useEffect(() => {
    const options = { root: null, rootMargin: "100px", threshold: 0.1 };

    observerRef.current = new IntersectionObserver((entries) => {
      const firstEntry = entries[0];
      if (
        firstEntry.isIntersecting &&
        hasMore &&
        !isLoadingMore &&
        !isInitialLoad
      ) {
        loadMoreUsers();
      }
    }, options);

    const currentTarget = loadMoreRef.current;
    if (currentTarget && !isLoading && !isInitialLoad && allUsers?.length > 0) {
      observerRef.current.observe(currentTarget);
    }

    return () => {
      if (currentTarget && observerRef.current) {
        observerRef.current.unobserve(currentTarget);
      }
    };
  }, [
    hasMore,
    isLoadingMore,
    isLoading,
    isInitialLoad,
    loadMoreUsers,
    allUsers,
  ]);

  // Show group form when user clicks arrow
  if (showGroupForm) {
    return (
      <GroupCreationForm
        onBack={handleBackFromGroupForm}
        selectedUserIds={checkedItems}
        onSubmit={handleGroupCreation}
      />
    );
  }

  return (
    <div className="chat-list-pane">
      {isLoading ? (
        <LoadingScreen />
      ) : (
        <>
          <List
            itemLayout="horizontal"
            dataSource={allUsers || []}
            renderItem={(user) => (
              <List.Item
                actions={
                  isGroupCreation
                    ? [
                        <Checkbox
                          checked={checkedItems.has(user?.id)}
                          onChange={() => handleCheckboxChange(user?.id)}
                        />,
                      ]
                    : []
                }
              >
                <List.Item.Meta
                  avatar={
                    <Avatar
                      {...(user.profile_picture && {
                        src: `${import.meta.env.VITE_API_BASE_URL}${user.profile_picture}`
                      })}
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
              <LoadingScreen />
            </div>
          )}

          {/* Intersection observer target */}
          {hasMore && !isLoadingMore && (
            <div ref={loadMoreRef} style={{ height: "20px" }} />
          )}

          {/* End of list */}
          {!hasMore && allUsers?.length > 0 && (
            <div style={{ textAlign: "center", padding: "20px", color: "#999" }}>
              No more users
            </div>
          )}
        </>
      )}

      {/* Floating Circle for Selected Count */}
      {isGroupCreation && checkedItems.size > 0 && (
        <Tooltip title={`Create group with ${checkedItems.size} selected user(s)`}>
          <div 
            className="selected-users-circle" 
            data-count={checkedItems.size}
            onClick={() => setShowGroupForm(true)}
          >
            <ArrowRightOutlined />
          </div>
        </Tooltip>
      )}
    </div>
  );
};

export default UserListPane;