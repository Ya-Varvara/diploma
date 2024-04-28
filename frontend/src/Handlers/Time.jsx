import moment from "moment";

export const MakePrettyDateTime = ({ datetime }) => {
  return moment.utc(datetime).local().format("YYYY-MM-DD HH:mm:ss");
};

export const MakePrettyTime = ({ time }) => {
  return moment.utc(`1970-01-01 ${time}`).local().format("HH:mm:ss");
};
