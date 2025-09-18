import pandas as pd

from core.application.get_stats.get_all_weather_stats_response import (
    GetAllWeatherStatsResponse,
)
from core.application.get_stats.get_precipitation_stats_response import (
    GetPrecipitationStatsResponse,
)
from core.application.get_stats.get_temperature_stats_response import (
    GetTemperatureStatsResponse,
)
from core.domain.models.all_weather_stats_by_city import AllWeatherStatsByCity
from core.domain.models.city_precipitation_stats import CityPrecipitationStats
from core.domain.models.city_temperature_stats import CityTemperatureStats
from core.domain.models.city_weather_stats import CityWeatherStats
from core.domain.models.precipitation_stats import PrecipitationStats
from core.domain.models.stats_query import StatsQuery
from core.domain.models.temperature_stats import TemperatureStats
from core.domain.repositories.city_repository import CityRepository
from core.domain.repositories.weather_data_repository import WeatherDataRepository


class GetStatsQuery:
    def __init__(
        self,
        city_repository: CityRepository,
        weather_data_repository: WeatherDataRepository,
    ):
        self.__city_repository = city_repository
        self.__weather_data_repository = weather_data_repository

    def execute_for_temperature(
        self,
        stats_query: StatsQuery,
    ) -> GetTemperatureStatsResponse:
        cities = self.__city_repository.get_cities_by_match(
            stats_query.city_name, stats_query.latitude, stats_query.longitude
        )

        city_temperature_stats = []
        for city in cities:
            weather_stats_df = pd.DataFrame(
                self.__weather_data_repository.get_by_city_id_and_date_range(
                    city.id, stats_query.start_date, stats_query.end_date
                ),
                columns=["date_time", "temperature"],
            )

            if weather_stats_df.empty:
                continue

            mean_temperature = self.__get_mean_from_df("temperature", weather_stats_df)
            mean_temperature_by_day = self.__get_mean_for_days(
                "temperature", weather_stats_df
            )

            max_temperature = self.__get_max("temperature", weather_stats_df)
            min_temperature = self.__get_min("temperature", weather_stats_df)

            hours_above_threshold = (
                weather_stats_df["temperature"] > stats_query.upper_threshold
            ).sum()
            hours_below_threshold = (
                weather_stats_df["temperature"] < stats_query.lower_threshold
            ).sum()

            city_temperature_stats.append(
                CityTemperatureStats(
                    longitude=city.longitude,
                    latitude=city.latitude,
                    temperature_stats=TemperatureStats(
                        average=mean_temperature,
                        average_by_day=mean_temperature_by_day,
                        max=max_temperature,
                        min=min_temperature,
                        hours_above_threshold=hours_above_threshold,
                        hours_below_threshold=hours_below_threshold,
                    ),
                )
            )

        return GetTemperatureStatsResponse(
            temperature_stats_for_cities=city_temperature_stats,
        )

    def execute_for_precipitation(
        self, stats_query: StatsQuery
    ) -> GetPrecipitationStatsResponse:
        cities = self.__city_repository.get_cities_by_match(
            stats_query.city_name, stats_query.latitude, stats_query.longitude
        )

        city_precipitation_stats = []
        for city in cities:
            weather_stats_df = pd.DataFrame(
                self.__weather_data_repository.get_by_city_id_and_date_range(
                    city.id, stats_query.start_date, stats_query.end_date
                ),
                columns=["date_time", "precipitation"],
            )

            if weather_stats_df.empty:
                continue

            mean_precipitation = self.__get_mean_from_df(
                "precipitation", weather_stats_df
            )
            total_precipitation = self.__get_sum_from_df(
                "precipitation", weather_stats_df
            )
            total_precipitation_by_day = self.__get_sum_for_days(
                "precipitation", weather_stats_df
            )
            days_with_precipitation = self.__get_day_with_precipitation(
                weather_stats_df
            )
            max_precipitation = self.__get_max("precipitation", weather_stats_df)

            city_precipitation_stats.append(
                CityPrecipitationStats(
                    longitude=city.longitude,
                    latitude=city.latitude,
                    precipitation_stats=PrecipitationStats(
                        total=total_precipitation,
                        total_by_day=total_precipitation_by_day,
                        days_with_precipitation=days_with_precipitation,
                        max=max_precipitation,
                        average=mean_precipitation,
                    ),
                )
            )

        return GetPrecipitationStatsResponse(
            precipitation_stats_for_cities=city_precipitation_stats,
        )

    def execute_for_all(self) -> GetAllWeatherStatsResponse:
        all_cities = self.__city_repository.get_all_cities()
        weather_stats_by_city = AllWeatherStatsByCity()

        for city in all_cities:
            weather_stats_df = pd.DataFrame(
                self.__weather_data_repository.get_by_city_id(city.id),
                columns=["date_time", "precipitation", "temperature"],
            )

            if weather_stats_df.empty:
                continue

            weather_stats_by_day = self.__get_df_with_day_column(weather_stats_df)

            start_date = weather_stats_by_day.loc[
                weather_stats_by_day["date_time"].idxmin()
            ]["day"]
            end_date = weather_stats_by_day.loc[
                weather_stats_by_day["date_time"].idxmax()
            ]["day"]

            mean_temperature = self.__get_mean_from_df("temperature", weather_stats_df)
            total_precipitation = self.__get_sum_from_df(
                "precipitation", weather_stats_df
            )
            days_with_precipitation = self.__get_day_with_precipitation(
                weather_stats_df
            )

            max_precipitation = self.__get_max("precipitation", weather_stats_df)
            max_temperature = self.__get_max("temperature", weather_stats_df)
            min_temperature = self.__get_min("temperature", weather_stats_df)

            weather_stats_by_city.all_city_weather_stats[city.name].append(
                CityWeatherStats(
                    latitude=city.latitude,
                    longitude=city.longitude,
                    start_date=start_date,
                    end_date=end_date,
                    temperature_average=mean_temperature,
                    precipitation_total=total_precipitation,
                    days_with_precipitation=days_with_precipitation,
                    precipitation_max=max_precipitation,
                    temperature_max=max_temperature,
                    temperature_min=min_temperature,
                )
            )

        return GetAllWeatherStatsResponse(weather_stats_by_city=weather_stats_by_city)

    def __get_day_with_precipitation(self, df: pd.DataFrame) -> int:
        return (df["precipitation"] > 0.0).sum()

    def __get_mean_from_df(self, column_name: str, df: pd.DataFrame) -> float:
        return df[column_name].mean()

    def __get_sum_from_df(self, column_name: str, df: pd.DataFrame) -> float:
        return df[column_name].sum()

    def __get_mean_for_days(
        self, column_name: str, df: pd.DataFrame
    ) -> dict[str, float]:
        df = self.__get_df_with_day_column(df)
        daily_mean = df.groupby("day")[column_name].mean()
        return daily_mean.to_dict()

    def __get_sum_for_days(
        self, column_name: str, df: pd.DataFrame
    ) -> dict[str, float]:
        df = self.__get_df_with_day_column(df)
        daily_sum = df.groupby("day")[column_name].sum()
        return daily_sum.to_dict()

    def __get_df_with_day_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy["day"] = df_copy["date_time"].dt.strftime("%Y-%m-%d")
        return df_copy

    def __get_max(self, column_name: str, df: pd.DataFrame) -> dict[str, float | str]:
        formatted_df = self.__format_df_for_max_min(df)
        return formatted_df.loc[formatted_df[column_name].idxmax()][
            ["date_time", column_name]
        ].to_dict()

    def __get_min(self, column_name: str, df: pd.DataFrame) -> dict[str, float | str]:
        formatted_df = self.__format_df_for_max_min(df)
        return formatted_df.loc[formatted_df[column_name].idxmin()][
            ["date_time", column_name]
        ].to_dict()

    def __format_df_for_max_min(self, df: pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy["date_time"] = df_copy["date_time"].dt.strftime("%Y-%m-%dT%H:%M")
        return df_copy
