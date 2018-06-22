/*
* @Author: robertking
* @Date:   2018-06-20 00:21:06
* @Last Modified by:   robertking
* @Last Modified time: 2018-06-22 22:51:51
*/


#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <utility>
#include <Python.h>
#include <algorithm>

#include <omp.h>
#include <emmintrin.h>

#include <cassert>
#include <float.h>

double sf = 13;

struct Point {
    double lng, lat;
    bool operator<(const Point &rhs) const
    { return (lng - 104) + (lat - 30.6) * sf < (rhs.lng - 104) + (rhs.lat - 30.6) * sf; }
};

class PyDoubleStr
{
private:
    char *s;
public:
    PyDoubleStr(double x) : s(PyOS_double_to_string(x, 'r', 0, Py_DTSF_ADD_DOT_0, NULL)) {}
    char *get() { return s; }
    PyDoubleStr(const PyDoubleStr &other) = delete;
    PyDoubleStr(PyDoubleStr &&other) { s = other.s; other.s = nullptr; }
    ~PyDoubleStr() { free(s); }
};

int getNext(const Point *centers, const Point point, const int k)
{
    int idx = 0;
    double dn = DBL_MAX;
    for (int i = 0; i < k; ++i) {
        double dlat = centers[i].lat - point.lat;
        double dlng = centers[i].lng - point.lng;
        double d = dlng * dlng + dlat * dlat;
        if (d < dn) {
            dn = d;
            idx = i;
        }
    }
    // printf("%d\t", idx);
    return idx;
}

int filterEmpty(Point *points, int *count, const int point_cnt)
{
    int res = 0;
    for (int i = 0; i < point_cnt; ++i) {
        if (count[i]) {
            points[res] = points[i];
            count[res] = count[i];
            ++res;
        }
    }
    printf("%d %d\n", res, point_cnt - res);
    return res;
}

void writeJSON(const char *filename, const Point *points, const int point_cnt, const int *count = nullptr)
{
    const static char *end[] = {", ", ""};
    FILE *file = fopen(filename, "w");
    fprintf(file, "var heatmapData = [");
    for (int i = 0; i < point_cnt; ++i) {
        fprintf(file, "{'lng': %s, 'lat': %s, 'count': %d}%s",
                PyDoubleStr(points[i].lng).get(), PyDoubleStr(points[i].lat).get(),
                count ? count[i] : 1,
                end[i == point_cnt - 1]);
    }
    fprintf(file, "];\n");
    fclose(file);
}

double eps = 0.00005;

Point *ema(const Point *points, int *tags, const int point_cnt,
           int *count, const int k)
{
    double maxx, minx, maxy, miny;
    maxx = minx = points[0].lng;
    maxy = miny = points[0].lat;

    for (int i = 1; i < point_cnt; ++i) {
        maxx = std::max(maxx, points[i].lng);
        minx = std::min(minx, points[i].lng);
        maxy = std::max(maxy, points[i].lat);
        miny = std::min(miny, points[i].lat);
    }

    Point *centers = (Point *)malloc(sizeof(Point) * k);
    Point *next_centers = (Point *)malloc(sizeof(Point) * k);

    int gridx = sqrt(k), gridy = k / gridx;
    assert(k % gridx == 0);
    for (int i = 0; i < gridx; ++i) {
        for (int j = 0; j < gridy; ++j) {
            centers[i * gridy + j].lng = minx + (maxx - minx) * (i + 0.5) / gridx;
            centers[i * gridy + j].lat = miny + (maxy - miny) * (j + 0.5) / gridy;
        }
    }

    for (int i = 0; i < point_cnt % k; ++i) {
        double lng = 0, lat = 0;
        const Point *p = points + (point_cnt / k + 1) * i;
        for (int j = 0; j < point_cnt / k + 1; ++j) {
            lng += p[j].lng;
            lat += p[j].lat;
        }
        centers[i].lng = lng / (point_cnt / k + 1);
        centers[i].lat = lat / (point_cnt / k + 1);
    }
    for (int i = point_cnt % k; i < k; ++i) {
        double lng = 0, lat = 0;
        const Point *p = points + (point_cnt / k) * i + point_cnt % k;
        for (int j = 0; j < point_cnt / k; ++j) {
            lng += p[j].lng;
            lat += p[j].lat;
        }
        centers[i].lng = lng / (point_cnt / k);
        centers[i].lat = lat / (point_cnt / k);
    }

    for (int i = 0; i < k; ++i) {
        centers[i] = points[i];
    }

    writeJSON("init_centers.js", centers, k);

    int iter_cnt = 0;
    while (true) {
        #pragma omp parallel for
        for (int i = 0; i < point_cnt; ++i)
            tags[i] = getNext(centers, points[i], k);

        #pragma omp parallel for
        for (int i = 0; i < k; ++i)
            next_centers[i].lat = next_centers[i].lng = count[i] = 0;

        for (int i = 0; i < point_cnt; ++i) {
            next_centers[tags[i]].lng += points[i].lng;
            next_centers[tags[i]].lat += points[i].lat;
            ++count[tags[i]];
        }

        for (int i = 0; i < k; ++i) {
            if (count[i]) {
                next_centers[i].lng /= count[i];
                next_centers[i].lat /= count[i];
            } else {
                next_centers[i].lng = centers[i].lng;
                next_centers[i].lat = centers[i].lat;
            }
        }

        double ep = 0;
        for (int i = 0; i < k; ++i) {
            double dlng = next_centers[i].lng - centers[i].lng;
            double dlat = next_centers[i].lat - centers[i].lat;
            double d = dlng * dlng + dlat * dlat;
            ep = std::max(ep, d);
        }
        ep = sqrt(ep);
        std::swap(centers, next_centers);

        printf("%s\t%d\n", PyDoubleStr(ep).get(), ++iter_cnt);
        if (ep < eps) break;
    }

    free(next_centers);

    return centers;
}

int main(int argc, char const *argv[])
{
    int k = 8000;
    if (argc > 1) k = atoi(argv[1]);
    if (argc > 2) eps = atof(argv[2]);
    if (argc > 3) sf = atof(argv[3]);

    Point *points = (Point *)malloc(sizeof(Point) * 200000);
    int point_cnt = 0;

    FILE *fin = fopen("../didi_data/order_sorted", "r");
    // while (fscanf(fin, "%*[^,],%*d,%*d,%*lf,%*lf,%lf,%lf", &points[point_cnt].lng, &points[point_cnt].lat) == 2)
    while (fscanf(fin, "%*[^,],%*d,%*d,%lf,%lf,%*lf,%*lf", &points[point_cnt].lng, &points[point_cnt].lat) == 2)
        ++point_cnt;
    fclose(fin);

    std::random_shuffle(points, points + point_cnt);

    writeJSON("clusters_raw.js", points, point_cnt);

    printf("%d\n", point_cnt);

    int *tags = (int *)malloc(sizeof(int) * point_cnt);
    int *count = (int *)malloc(sizeof(int) * k);

    Point *centers = ema(points, tags, point_cnt, count, k);

    int new_k = filterEmpty(centers, count, k);

    // writeJSON("clusters_end_cpp.js", centers, new_k, count);
    writeJSON("clusters_start_cpp.js", centers, new_k, count);

    free(centers);
    free(count);
    free(points);
    free(tags);

    return 0;
}
