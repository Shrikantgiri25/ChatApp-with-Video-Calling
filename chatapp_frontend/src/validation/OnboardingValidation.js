import * as Yup from "yup";

export const OnBoardingSchema = Yup.object().shape({
  bio: Yup.string()
    .max(50, "Max 50 characters"),
  profile_picture: Yup.mixed()
    .nullable(),
});
