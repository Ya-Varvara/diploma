import moment from "moment";

export const MakePrettyDateTime = ({ datetime }) => {
  return moment.utc(datetime).local().format("YYYY-MM-DD HH:mm:ss");
};

export const MakePrettyTime = ({ time }) => {
  return moment.utc(time).local().format("HH:mm:ss");
};
