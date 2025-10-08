import * as Yup from 'yup';

export const GroupCreationSchema = Yup.object().shape({
  group_name: Yup.string()
    .min(3, 'Group name must be at least 3 characters')
    .max(50, 'Group name must be at most 50 characters')
    .required('Group name is required'),
  description: Yup.string()
    .max(100, 'Description must be at most 100 characters'),
  group_avatar: Yup.mixed()
});